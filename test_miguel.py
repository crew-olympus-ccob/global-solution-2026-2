import os, sys, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from erros import (EntradaVaziaError, TemaInexistenteError, AmbiguidadeError,
                   ErroDeBusca, mensagem_amigavel)
from busca_tema import listar_temas, buscar_por_tema
from respostas import modelo_1_direto_tecnico

def _r(i, tema):
    return {"id": i, "tema": tema, "pergunta_chave": f"pergunta {i}?",
            "conteudo": f"conteudo {i}", "referencia": "fonte", "data_verificacao": "2026-11-12"}

BASE = [_r(1, "Documentação"), _r(6, "Direitos"), _r(11, "Serviços"), _r(12, "Serviços")]


class TestBuscaTema(unittest.TestCase):
    def test_ordem_dos_temas(self):
        self.assertEqual(listar_temas(BASE), ["Direitos", "Documentação", "Serviços"])

    def test_nome_exato_sem_acento(self):
        tema, regs = buscar_por_tema(BASE, "servicos")
        self.assertEqual((tema, len(regs)), ("Serviços", 2))

    def test_trecho_unico(self):
        self.assertEqual(buscar_por_tema(BASE, "ser")[0], "Serviços")

    def test_numero_da_opcao(self):
        self.assertEqual(buscar_por_tema(BASE, "3")[0], "Serviços")


class TestErros(unittest.TestCase):
    def test_vazia(self):
        for x in ("", "   ", None):
            with self.assertRaises(EntradaVaziaError):
                buscar_por_tema(BASE, x)

    def test_inexistente(self):
        with self.assertRaises(TemaInexistenteError):
            buscar_por_tema(BASE, "xyz")
        with self.assertRaises(TemaInexistenteError):
            buscar_por_tema(BASE, "9")

    def test_ambiguo(self):
        with self.assertRaises(AmbiguidadeError) as c:
            buscar_por_tema(BASE, "s")          # 'Direitos' e 'Serviços'
        self.assertIn("Direitos", mensagem_amigavel(c.exception))

    def test_todos_herdam_de_erro_de_busca(self):
        for exc in (EntradaVaziaError, TemaInexistenteError, AmbiguidadeError):
            self.assertTrue(issubclass(exc, ErroDeBusca))


class TestModelo1(unittest.TestCase):
    def test_formato(self):
        txt = modelo_1_direto_tecnico(BASE[2], rodape="AVISO")
        self.assertTrue(txt.startswith("[SERVIÇOS] pergunta 11?"))
        self.assertTrue(txt.endswith("AVISO"))
        self.assertIn("verificado em 2026-11-12", txt)


class TestServicosJson(unittest.TestCase):
    def test_estrutura(self):
        import json
        caminho = os.path.join(os.path.dirname(__file__), "..", "data", "servicos.json")
        with open(caminho, encoding="utf-8") as f:
            regs = json.load(f)
        self.assertEqual([r["id"] for r in regs], [11, 12, 13, 14, 15])
        campos = {"id", "tema", "pergunta_chave", "conteudo", "referencia", "data_verificacao"}
        for r in regs:
            self.assertEqual(set(r), campos)
            self.assertEqual(r["tema"], "Serviços")
            self.assertTrue(all(str(v).strip() for v in r.values()))


if __name__ == "__main__":
    unittest.main(verbosity=2)
