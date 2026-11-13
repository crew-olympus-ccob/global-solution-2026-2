import builtins
import io
import json
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import date
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

import base
import busca
import indicador
import navegacao
import saida

FIXTURE = RAIZ / "tests" / "fixtures" / "base_teste.json"


def _json_temp(conteudo) -> Path:
    f = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    f.write(conteudo if isinstance(conteudo, str) else json.dumps(conteudo, ensure_ascii=False))
    f.close()
    return Path(f.name)


def _registros_brutos():
    return json.loads(FIXTURE.read_text(encoding="utf-8"))


class TestBase(unittest.TestCase):
    def test_carrega_fixture(self):
        self.assertEqual(len(base.carregar_base(FIXTURE)), 15)

    def test_base_real_e_valida(self):
        self.assertGreater(len(base.carregar_base()), 0)

    def test_arquivo_inexistente(self):
        with self.assertRaisesRegex(base.ErroBase, "não encontrado"):
            base.carregar_base("nao_existe.json")

    def test_json_quebrado(self):
        with self.assertRaisesRegex(base.ErroBase, "corrompido"):
            base.carregar_base(_json_temp('[ {"id": 1,  } ]'))

    def test_mensagem_sem_erro_duplicado(self):
        try:
            base.carregar_base("nao_existe.json")
        except base.ErroBase as e:
            self.assertFalse(str(e).startswith("Erro:"))

    def test_formato_errado_nao_e_lista(self):
        with self.assertRaisesRegex(base.ErroBase, "lista"):
            base.carregar_base(_json_temp({"registros": []}))

    def test_base_vazia(self):
        with self.assertRaisesRegex(base.ErroBase, "nenhum registro"):
            base.carregar_base(_json_temp([]))

    def test_campo_obrigatorio_faltando(self):
        reg = _registros_brutos()[0]
        del reg["referencia"]
        with self.assertRaisesRegex(base.ErroBase, "referencia"):
            base.carregar_base(_json_temp([reg]))

    def test_id_invalido(self):
        for ruim in ["abc", 1.5, True, "-1"]:
            reg = dict(_registros_brutos()[0], id=ruim)
            with self.assertRaisesRegex(base.ErroBase, "inteiro", msg=ruim):
                base.carregar_base(_json_temp([reg]))

    def test_id_texto_numerico_vira_int(self):
        reg = dict(_registros_brutos()[0], id="7")
        self.assertEqual(base.carregar_base(_json_temp([reg]))[0]["id"], 7)

    def test_data_em_formato_errado(self):
        reg = dict(_registros_brutos()[0], data_verificacao="12/11/2026")
        with self.assertRaisesRegex(base.ErroBase, "AAAA-MM-DD"):
            base.carregar_base(_json_temp([reg]))

    def test_id_repetido(self):
        regs = _registros_brutos()[:2]
        regs[1]["id"] = regs[0]["id"]
        with self.assertRaisesRegex(base.ErroBase, "repetido"):
            base.carregar_base(_json_temp(regs))

    def test_campos_opcionais_ausentes_viram_vazios(self):
        r = base.carregar_base(FIXTURE)[0]
        self.assertEqual((r["palavras_chave"], r["passos"], r["alerta"]), ([], [], ""))


class TestBusca(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.regs = base.carregar_base(FIXTURE)

    def _ids(self, consulta):
        return [r["id"] for r in busca.empate_no_topo(consulta, self.regs)]

    def test_normalizar_acentos_e_caixa(self):
        self.assertEqual(busca.normalizar("  CADÚNICO, Cartão!! "), "cadunico cartao")

    def test_radical(self):
        r = busca._radical
        self.assertEqual(r("comprei"), r("compra"))
        self.assertEqual(r("arrependi"), r("arrependimento"))
        self.assertNotEqual(r("compra"), r("comprovante"))
        self.assertNotEqual(r("consumidor"), r("consultar"))
        self.assertEqual(r("cpf"), "cpf")

    def test_perguntas_do_gabriel(self):
        self.assertEqual(self._ids("Perdi meu CPF, como tiro a segunda via?"), [2])
        self.assertEqual(self._ids("Como emitir a certidão de antecedentes criminais?"), [5])

    def test_funciona_sem_palavras_chave(self):
        self.assertEqual(self._ids("vacina"), [13])

    def test_palavras_chave_ajudam(self):
        self.assertEqual(self._ids("o produto estragou"), [7])

    def test_erro_de_digitacao(self):
        self.assertEqual(self._ids("identidae nova"), [1])

    def test_nada_encontrado(self):
        for q in ["receita de bolo", "", "   ", "de para com", "documento do carro"]:
            self.assertEqual(self._ids(q), [], q)

    def test_conteudo_sozinho_nao_responde(self):
        self.assertEqual(self._ids("aplicativo biometria"), [])

    def test_expressao_composta_so_vale_inteira(self):
        reg = dict(self.regs[2], palavras_chave=["multa eleitoral"])
        self.assertEqual(busca.pontuar("multa de transito", reg), 0)
        self.assertGreater(busca.pontuar("tenho multa eleitoral", reg), 0)

    def test_empate_devolve_varios(self):
        self.assertEqual(sorted(self._ids("cancelar compra")), [6, 9])

    def test_buscar_por_id(self):
        self.assertEqual(busca.buscar_por_id(" 2 ", self.regs)["id"], 2)
        self.assertEqual(busca.buscar_por_id(2, self.regs)["id"], 2)
        for ruim in ["99", "abc", "", "²", "-1"]:
            self.assertIsNone(busca.buscar_por_id(ruim, self.regs), ruim)

    def test_escolher_por_numero_rejeita_lixo(self):
        opcoes = ["a", "b", "c"]
        self.assertEqual(busca.escolher_por_numero("2", opcoes), "b")
        for lixo in ["", " ", "0", "4", "-1", "1.5", "²", "um", "1e3", "999999999999999999999"]:
            self.assertIsNone(busca.escolher_por_numero(lixo, opcoes), lixo)

    def test_temas_na_ordem_da_base(self):
        self.assertEqual(busca.listar_temas(self.regs)[0], "Documentação")
        self.assertEqual(len(busca.listar_temas(self.regs)), 3)


class TestModelo2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.regs = base.carregar_base(FIXTURE)
        cls.cpf = cls.regs[1]
        cls.rico = cls.regs[5]

    def test_dividir_frases(self):
        frases = saida.dividir_frases("Acesse gov.br/identidade. Leve o RG. Pronto!")
        self.assertEqual(frases, ["Acesse gov.br/identidade.", "Leve o RG.", "Pronto!"])

    def test_so_campos_obrigatorios(self):
        txt = saida.modelo_2_educativo(self.cpf, self.regs, "Aviso X", hoje=date(2026, 11, 12))
        for secao in ["EM RESUMO", "COMO FAZER", "ATENÇÃO", "FONTE", "VEJA TAMBÉM", "Aviso: Aviso X"]:
            self.assertIn(secao, txt)
        self.assertIn("! Desconfie", txt)
        self.assertNotIn("PASSO A PASSO", txt)
        self.assertIn("verificada em 12/11/2026", txt)

    def test_com_passos_e_alerta(self):
        txt = saida.modelo_2_educativo(self.rico, self.regs, "")
        self.assertIn("PASSO A PASSO", txt)
        self.assertIn("1. Passo de teste 1.", txt)
        self.assertIn("ENTENDA MELHOR", txt)
        self.assertIn("! Alerta de teste.", txt)

    def test_omite_secoes_vazias(self):
        reg = dict(self.cpf, conteudo="Frase única.")
        txt = saida.modelo_2_educativo(reg, None, "")
        for secao in ["COMO FAZER", "PASSO A PASSO", "ATENÇÃO", "VEJA TAMBÉM", "Aviso:"]:
            self.assertNotIn(secao, txt)
        self.assertIn("EM RESUMO", txt)

    def test_veja_tambem_usa_navegacao(self):
        txt = saida.modelo_2_educativo(self.cpf, self.regs)
        self.assertIn("[1]", txt)
        self.assertNotIn("[2]", txt)
        self.assertNotIn("[6]", txt)

    def test_link_longo_nao_e_quebrado(self):
        url = "https://www.tse.jus.br/servicos-eleitorais/servicos/carta-de-servicos-ao-eleitor"
        txt = saida.modelo_2_educativo(dict(self.cpf, referencia=url), None, "")
        self.assertIn(f"  {url}", txt.splitlines())

    def test_alerta_de_informacao_antiga(self):
        txt = saida.modelo_2_educativo(self.cpf, None, "", hoje=date(2028, 1, 1))
        self.assertIn("mais de 1 ano", txt)

    def test_linhas_respeitam_largura(self):
        reg = dict(self.cpf, conteudo="Palavra " * 80 + ".")
        txt = saida.modelo_2_educativo(reg, self.regs)
        self.assertTrue(all(len(l) <= saida.LARGURA for l in txt.splitlines() if "http" not in l))

    def test_modelo_1_mesma_assinatura(self):
        txt = saida.modelo_1_direto(self.cpf, self.regs, "Aviso")
        self.assertIn(self.cpf["conteudo"], txt)


class TestNavegacaoCorrigida(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.regs = base.carregar_base(FIXTURE)

    def _escolher(self, entradas):
        with mock.patch.object(builtins, "input", side_effect=entradas), redirect_stdout(io.StringIO()):
            return navegacao.escolher_relacionado(self.regs, self.regs[0])

    def test_superescrito_nao_quebra(self):
        self.assertEqual(self._escolher(["²", "1"])["id"], 2)

    def test_ctrl_d_volta_sem_erro(self):
        self.assertIsNone(self._escolher(EOFError()))

    def test_lixo_e_zero(self):
        self.assertIsNone(self._escolher(["", "abc", "-1", "99", "0"]))


class TestIndicador(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.regs = base.carregar_base(FIXTURE)

    def test_calculo_da_taxa(self):
        casos = [
            {"pergunta": "perdi meu cpf", "id_esperado": 2},
            {"pergunta": "perdi meu cpf", "id_esperado": 1},
            {"pergunta": "receita de bolo", "id_esperado": None},
            {"pergunta": "1>2", "id_esperado": 2, "forma": "menu"},
        ]
        res = indicador.calcular(self.regs, casos)
        self.assertEqual((res["acertos"], res["avaliados"]), (3, 4))
        self.assertEqual(res["taxa"], 75.0)
        self.assertEqual(res["por_forma"], {"menu": 100.0, "palavra_chave": 66.7})

    def test_ambiguo_conta_como_erro(self):
        r = indicador.executar_caso({"pergunta": "cancelar compra", "id_esperado": 6}, self.regs)
        self.assertFalse(r["acerto"])
        self.assertIn("ambíguo", r["motivo"])

    def test_pendente_fica_fora_da_conta(self):
        base5 = self.regs[:5]
        res = indicador.calcular(base5, [
            {"pergunta": "perdi meu cpf", "id_esperado": 2},
            {"pergunta": "farmacia popular", "id_esperado": 12},
        ])
        self.assertEqual((res["avaliados"], res["pendentes"], res["taxa"]), (1, 1, 100.0))

    def test_falso_positivo_de_pendente_conta_como_erro(self):
        base5 = self.regs[:5]
        r = indicador.executar_caso({"pergunta": "segunda via do cpf", "id_esperado": 99}, base5)
        self.assertFalse(r["pendente"])
        self.assertIn("falso positivo", r["motivo"])

    def test_menu_tema_assunto(self):
        self.assertEqual(indicador.resolver_menu("3>5", self.regs)[0]["id"], 15)
        for ruim in ["9>1", "1>9", ">", "abc", ""]:
            self.assertEqual(indicador.resolver_menu(ruim, self.regs), [], ruim)

    def test_lista_vazia(self):
        self.assertEqual(indicador.taxa_de_acerto([]), 0.0)

    def test_perguntas_oficiais_carregam(self):
        self.assertGreater(len(indicador.carregar_casos()), 0)


if __name__ == "__main__":
    unittest.main()
