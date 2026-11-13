"""Testes da parte do Miguel. Rodar na raiz do repositório:

    python -m unittest tests/test_miguel.py -v      (ou: pytest tests/test_miguel.py)
"""

import json
import re
import sys
import unittest
from datetime import datetime
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RAIZ / "src"))

from busca_tema import buscar_por_tema, listar_temas, normalizar, resolver_tema  # noqa: E402
from erros import (AmbiguidadeError, EntradaVaziaError, ErroDeConsulta,  # noqa: E402
                   TemaInexistenteError, escolher_opcao, executar_seguro)
from respostas import formatar_modelo_1  # noqa: E402

CAMPOS = {"id", "tema", "pergunta_chave", "conteudo", "referencia", "data_verificacao"}

with open(RAIZ / "data" / "servicos.json", encoding="utf-8") as f:
    SERVICOS = json.load(f)

# Base de teste com os 3 temas (Documentação e Direitos são só marcadores).
BASE = [
    {"id": 1, "tema": "Documentação", "pergunta_chave": "CIN?", "conteudo": "x", "referencia": "r", "data_verificacao": "2026-11-13"},
    {"id": 6, "tema": "Direitos", "pergunta_chave": "Arrependimento?", "conteudo": "x", "referencia": "r", "data_verificacao": "2026-11-13"},
] + SERVICOS


class TestJsonServicos(unittest.TestCase):
    def test_cinco_registros_ids_11_a_15(self):
        self.assertEqual([r["id"] for r in SERVICOS], [11, 12, 13, 14, 15])

    def test_campos_padronizados(self):
        for r in SERVICOS:
            self.assertEqual(set(r), CAMPOS, f"id {r['id']}")

    def test_conteudo_preenchido_e_tema_correto(self):
        for r in SERVICOS:
            self.assertEqual(r["tema"], "Serviços")
            self.assertGreater(len(r["conteudo"]), 150, f"id {r['id']} curto demais")
            self.assertTrue(r["pergunta_chave"].endswith("?"))

    def test_referencia_tem_url_e_data_valida(self):
        for r in SERVICOS:
            self.assertRegex(r["referencia"], r"https?://")
            datetime.strptime(r["data_verificacao"], "%Y-%m-%d")


class TestBuscaPorTema(unittest.TestCase):
    def test_por_numero(self):
        tema, regs = buscar_por_tema(BASE, "3")
        self.assertEqual(tema, "Serviços")
        self.assertEqual([r["id"] for r in regs], [11, 12, 13, 14, 15])

    def test_por_nome_com_e_sem_acento_e_caixa(self):
        for entrada in ("Serviços", "servicos", "  SERVIÇOS  "):
            self.assertEqual(resolver_tema(BASE, entrada), "Serviços")

    def test_por_palavra_relacionada(self):
        for entrada in ("vacina", "farmácia popular", "cadunico", "SUS", "isenção de concurso"):
            self.assertEqual(resolver_tema(BASE, entrada), "Serviços", entrada)
        self.assertEqual(resolver_tema(BASE, "procon"), "Direitos")
        self.assertEqual(resolver_tema(BASE, "cpf"), "Documentação")

    def test_tolera_erro_de_digitacao(self):
        self.assertEqual(resolver_tema(BASE, "servisos"), "Serviços")
        self.assertEqual(resolver_tema(BASE, "vacinaçao"), "Serviços")

    def test_listar_temas_ordem_e_sem_repeticao(self):
        self.assertEqual(listar_temas(BASE), ["Documentação", "Direitos", "Serviços"])

    def test_normalizar(self):
        self.assertEqual(normalizar("  Documentação   Cívil "), "documentacao civil")


class TestCenariosDeErro(unittest.TestCase):
    def test_1_entrada_vazia(self):
        for entrada in ("", "   ", None, "\t\n"):
            with self.assertRaises(EntradaVaziaError):
                resolver_tema(BASE, entrada)

    def test_2_tema_inexistente(self):
        for entrada in ("futebol", "99", "0", "-1"):
            with self.assertRaises(TemaInexistenteError, msg=entrada):
                resolver_tema(BASE, entrada)

    def test_2_tema_inexistente_lista_opcoes(self):
        with self.assertRaises(TemaInexistenteError) as ctx:
            resolver_tema(BASE, "futebol")
        self.assertIn("Serviços", ctx.exception.mensagem)
        self.assertEqual(ctx.exception.temas_disponiveis, ["Documentação", "Direitos", "Serviços"])

    def test_3_ambiguidade(self):
        for entrada in ("carteira", "cadastro"):
            with self.assertRaises(AmbiguidadeError, msg=entrada) as ctx:
                resolver_tema(BASE, entrada)
            self.assertEqual(set(ctx.exception.opcoes), {"Documentação", "Serviços"})

    def test_executar_seguro_nao_quebra(self):
        for entrada in ("", "futebol", "carteira"):
            ok, erro = executar_seguro(buscar_por_tema, BASE, entrada)
            self.assertFalse(ok)
            self.assertIsInstance(erro, ErroDeConsulta)
            self.assertTrue(erro.mensagem)
        ok, (tema, _) = executar_seguro(buscar_por_tema, BASE, "vacina")
        self.assertTrue(ok)
        self.assertEqual(tema, "Serviços")

    def test_escolher_opcao(self):
        def fake(respostas):
            it = iter(respostas)
            return lambda _prompt: next(it)
        silencio = lambda *_: None
        self.assertEqual(escolher_opcao(["a", "b"], fake(["2"]), silencio), 1)
        self.assertIsNone(escolher_opcao(["a", "b"], fake([""]), silencio))
        self.assertEqual(escolher_opcao(["a", "b"], fake(["x", "9", "1"]), silencio), 0)
        self.assertIsNone(escolher_opcao(["a", "b"], fake(["x", "y", "z"]), silencio))

        def eof(_):
            raise EOFError
        self.assertIsNone(escolher_opcao(["a"], eof, silencio))


class TestModelo1(unittest.TestCase):
    def test_contem_blocos_obrigatorios(self):
        for r in SERVICOS:
            texto = formatar_modelo_1(r)
            for bloco in ("PERGUNTA:", "PROCEDIMENTO:", "FONTE:", "VERIFICADO EM:", "AVISO:"):
                self.assertIn(bloco, texto, f"id {r['id']} sem {bloco}")
            self.assertIn("13/11/2026", texto)
            self.assertIn("http", texto)

    def test_largura_maxima(self):
        for r in SERVICOS:
            for linha in formatar_modelo_1(r).splitlines():
                if "http" not in linha:  # URL nunca é quebrada, então pode passar da largura
                    self.assertLessEqual(len(linha), 90, linha)

    def test_url_nao_e_quebrada(self):
        texto = formatar_modelo_1(SERVICOS[1])
        self.assertIn("https://www.gov.br/saude/pt-br/composicao/sectics/farmacia-popular", texto)

    def test_nao_quebra_com_registro_incompleto_ou_texto_corrido(self):
        self.assertIn("sem conteúdo", formatar_modelo_1({}))
        corrido = {"id": 1, "tema": "X", "pergunta_chave": "?", "conteudo": "Texto corrido sem passos.",
                   "referencia": "", "data_verificacao": "lixo"}
        texto = formatar_modelo_1(corrido)
        self.assertIn("RESPOSTA:", texto)
        self.assertIn("não informada", texto)

    def test_rodape_customizado(self):
        texto = formatar_modelo_1(SERVICOS[0], rodape=lambda r: "RODAPE-DO-LUCAS")
        self.assertTrue(texto.rstrip().endswith("RODAPE-DO-LUCAS"))
        self.assertNotIn("AVISO:", texto)


if __name__ == "__main__":
    unittest.main(verbosity=2)
