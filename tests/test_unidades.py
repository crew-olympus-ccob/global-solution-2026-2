import builtins
import importlib.util
import io
import sys
import unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

import busca  # noqa: E402
import carregador  # noqa: E402
import indicador  # noqa: E402
import navegacao  # noqa: E402
import saida  # noqa: E402

FIXTURE = str(RAIZ / "tests" / "fixtures" / "base_teste.json")
CAMPOS = ("id", "tema", "pergunta_chave", "conteudo", "referencia", "data_verificacao")
TEM_BUSCA_TEMA = importlib.util.find_spec("busca_tema") is not None
TEM_RESPOSTAS = importlib.util.find_spec("respostas") is not None


def _carregar(caminho=None):
    with redirect_stdout(io.StringIO()):
        return carregador.carregar_base(caminho) if caminho else carregador.carregar_base()


class TestLeituraDaBase(unittest.TestCase):
    def test_base_real_carrega(self):
        base = _carregar()
        self.assertGreater(len(base), 0)
        self.assertEqual(len({r["id"] for r in base}), len(base))

    def test_registros_tem_os_campos_combinados(self):
        for r in _carregar():
            for campo in CAMPOS:
                self.assertTrue(r.get(campo), f"registro {r.get('id')} sem {campo}")

    def test_arquivo_inexistente_nao_quebra(self):
        self.assertEqual(_carregar("nao_existe.json"), [])


class TestBuscaPorPergunta(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = _carregar(FIXTURE)

    def _primeiro(self, consulta):
        r = busca.buscar_por_pergunta(consulta, self.base)
        return r[0]["id"] if r else None

    def test_devolve_lista_de_registros(self):
        r = busca.buscar_por_pergunta("perdi meu cpf", self.base)
        self.assertIsInstance(r, list)
        self.assertTrue(all(isinstance(x, dict) and "id" in x for x in r))

    def test_perguntas_do_gabriel(self):
        casos = {
            "Perdi meu CPF, como tiro a segunda via?": 2,
            "Como faço para tirar a nova identidade?": 1,
            "Como consultar a situação do meu título de eleitor?": 3,
            "Como acessar a minha carteira de trabalho digital?": 4,
            "Como emitir a certidão de antecedentes criminais?": 5,
        }
        for pergunta, esperado in casos.items():
            self.assertEqual(self._primeiro(pergunta), esperado, pergunta)

    def test_cada_registro_e_achado_pela_propria_pergunta(self):
        base = _carregar()
        for r in base:
            achados = busca.buscar_por_pergunta(r["pergunta_chave"], base)
            self.assertTrue(achados and achados[0]["id"] == r["id"], r["pergunta_chave"])

    def test_entrada_vazia_ou_so_stopwords(self):
        for q in ["", "   ", "de para com"]:
            self.assertEqual(busca.buscar_por_pergunta(q, self.base), [], q)

    def test_entradas_estranhas_nao_quebram(self):
        for q in ["a" * 5000, "\U0001F642" * 3, "²", "'; DROP TABLE x; --", "\x00", "%s {0}", "1e9", "-1"]:
            self.assertIsInstance(busca.buscar_por_pergunta(q, self.base), list, repr(q[:10]))


@unittest.skipUnless(TEM_BUSCA_TEMA, "aguardando src/busca_tema.py (busca por tema)")
class TestBuscaPorTema(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        import busca_tema
        cls.bt = busca_tema
        cls.base = _carregar()

    def test_cada_tema_devolve_so_os_seus_registros(self):
        for tema in {r["tema"] for r in self.base}:
            achado, registros = self.bt.buscar_por_tema(self.base, tema)
            self.assertEqual(achado, tema)
            self.assertTrue(registros and all(r["tema"] == tema for r in registros))

    def test_entrada_vazia_e_tratada(self):
        with self.assertRaises(Exception):
            self.bt.buscar_por_tema(self.base, "")


@unittest.skipUnless(TEM_RESPOSTAS, "aguardando src/respostas.py (Modelo 1)")
class TestModelo1(unittest.TestCase):
    def test_responde_todos_os_registros(self):
        from respostas import modelo_1_direto_tecnico
        for r in _carregar():
            texto = modelo_1_direto_tecnico(r)
            self.assertIsInstance(texto, str)
            self.assertTrue(texto.strip(), r["id"])


class TestModelo2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = _carregar(FIXTURE)
        cls.cpf = cls.base[1]
        cls.rico = cls.base[5]

    def test_dividir_frases(self):
        frases = saida.dividir_frases("Acesse gov.br/identidade. Leve o RG. Pronto!")
        self.assertEqual(frases, ["Acesse gov.br/identidade.", "Leve o RG.", "Pronto!"])

    def test_so_campos_obrigatorios(self):
        txt = saida.modelo_2_educativo(self.cpf, self.base)
        for secao in ["EM RESUMO", "COMO FAZER", "ATENÇÃO", "VEJA TAMBÉM"]:
            self.assertIn(secao, txt)
        self.assertIn("! Desconfie", txt)
        self.assertNotIn("PASSO A PASSO", txt)

    def test_com_passos_e_alerta(self):
        txt = saida.modelo_2_educativo(self.rico, self.base)
        self.assertIn("PASSO A PASSO", txt)
        self.assertIn("1. Passo de teste 1.", txt)
        self.assertIn("ENTENDA MELHOR", txt)
        self.assertIn("! Alerta de teste.", txt)

    def test_omite_secoes_vazias(self):
        txt = saida.modelo_2_educativo(dict(self.cpf, conteudo="Frase única."))
        for secao in ["COMO FAZER", "PASSO A PASSO", "ATENÇÃO", "VEJA TAMBÉM"]:
            self.assertNotIn(secao, txt)
        self.assertIn("EM RESUMO", txt)

    def test_recebe_fonte_e_aviso_de_fora(self):
        txt = saida.modelo_2_educativo(self.cpf, None, "Fonte: X\nAviso: Y")
        self.assertIn("Fonte: X\nAviso: Y", txt)
        self.assertNotIn("Fonte:", saida.modelo_2_educativo(self.cpf))

    def test_veja_tambem_usa_navegacao(self):
        txt = saida.modelo_2_educativo(self.cpf, self.base)
        self.assertIn("[1]", txt)
        self.assertNotIn("[2]", txt)
        self.assertNotIn("[6]", txt)

    def test_linhas_respeitam_largura(self):
        txt = saida.modelo_2_educativo(dict(self.cpf, conteudo="Palavra " * 80 + "."), self.base)
        self.assertTrue(all(len(l) <= saida.LARGURA for l in txt.splitlines()))

    def test_todos_os_registros_reais(self):
        base = _carregar()
        for r in base:
            self.assertIn("EM RESUMO", saida.modelo_2_educativo(r, base))


class TestValidacaoNavegacao(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = _carregar(FIXTURE)

    def _escolher(self, entradas):
        with mock.patch.object(builtins, "input", side_effect=entradas), redirect_stdout(io.StringIO()):
            return navegacao.escolher_relacionado(self.base, self.base[0])

    def test_lixo_e_zero(self):
        self.assertIsNone(self._escolher(["", "abc", "-1", "99", "0"]))

    @unittest.expectedFailure
    def test_superescrito_nao_quebra(self):
        self.assertEqual(self._escolher(["²", "1"])["id"], 2)

    @unittest.expectedFailure
    def test_ctrl_d_nao_quebra(self):
        self.assertIsNone(self._escolher(EOFError()))


class TestIndicador(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.base = _carregar(FIXTURE)

    def test_calculo_da_taxa(self):
        casos = [
            {"pergunta": "perdi meu cpf", "id_esperado": 2},
            {"pergunta": "perdi meu cpf", "id_esperado": 1},
            {"pergunta": "xyzw kkk", "id_esperado": None},
        ]
        res = indicador.calcular(self.base, casos)
        self.assertEqual((res["acertos"], res["avaliados"]), (2, 3))
        self.assertEqual(res["taxa"], 66.7)

    def test_so_o_primeiro_resultado_conta(self):
        r = indicador.executar_caso({"pergunta": "perdi meu cpf", "id_esperado": 11}, self.base)
        self.assertFalse(r["acerto"])
        self.assertEqual(r["obtido"], [2])

    def test_pendente_fica_fora_da_conta(self):
        res = indicador.calcular(self.base[:5], [
            {"pergunta": "perdi meu cpf", "id_esperado": 2},
            {"pergunta": "farmacia popular", "id_esperado": 12},
        ])
        self.assertEqual((res["avaliados"], res["pendentes"], res["taxa"]), (1, 1, 100.0))

    def test_falso_positivo_conta_como_erro(self):
        r = indicador.executar_caso({"pergunta": "segunda via do cpf", "id_esperado": 99}, self.base[:5])
        self.assertFalse(r["pendente"])
        self.assertIn("falso positivo", r["motivo"])

    def test_menu_aguarda_busca_por_tema(self):
        r = indicador.executar_caso({"pergunta": "Documentação>2", "id_esperado": 2, "forma": "menu"}, self.base, None)
        self.assertTrue(r["pendente"])
        self.assertIn("busca_tema", r["motivo"])

    def test_menu_com_busca_por_tema_simulada(self):
        def falsa(base, entrada):
            tema = next(t for t in sorted({r["tema"] for r in base}) if t.lower() == entrada.lower())
            return tema, [r for r in base if r["tema"] == tema]
        r = indicador.executar_caso({"pergunta": "Documentação>2", "id_esperado": 2, "forma": "menu"}, self.base, falsa)
        self.assertTrue(r["acerto"], r)

    def test_lista_vazia(self):
        self.assertEqual(indicador.taxa_de_acerto([]), 0.0)

    def test_perguntas_oficiais_carregam(self):
        self.assertGreater(len(indicador.carregar_casos()), 6)


if __name__ == "__main__":
    unittest.main()
