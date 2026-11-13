import os
import subprocess
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
MAIN = RAIZ / "src" / "main.py"
FIXTURE = RAIZ / "tests" / "fixtures" / "base_teste.json"


def rodar(entradas, *args, base=FIXTURE, timeout=15):
    texto = entradas if isinstance(entradas, str) else "\n".join(entradas) + "\n"
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    cmd = [sys.executable, str(MAIN)] + (["--base", str(base)] if base else []) + list(args)
    p = subprocess.run(cmd, input=texto, capture_output=True, text=True,
                       encoding="utf-8", timeout=timeout, env=env)
    return p.returncode, p.stdout, p.stderr


class TestDuasFormasDeBusca(unittest.TestCase):
    def test_forma1_palavra_chave(self):
        code, out, err = rodar(["1", "perdi meu CPF", "n", "0", "0"])
        self.assertEqual(code, 0, err)
        self.assertIn("COMO TIRAR A PRIMEIRA OU A SEGUNDA VIA DO CPF?", out)
        self.assertIn("Código: 2", out)
        self.assertIn("Até logo!", out)

    def test_forma2_menu_tema_assunto(self):
        code, out, err = rodar(["2", "3", "1", "n", "0", "0", "0"])
        self.assertEqual(code, 0, err)
        self.assertIn("Código: 11", out)

    def test_navegacao_relacionados_do_gabriel(self):
        code, out, err = rodar(["1", "perdi meu cpf", "s", "1", "n", "0", "0"])
        self.assertEqual(code, 0, err)
        self.assertIn("Outros assuntos de Documentação", out)
        self.assertIn("Código: 1", out)

    def test_forma1_empate_pergunta_ao_usuario(self):
        code, out, _ = rodar(["1", "cancelar compra", "2", "n", "0", "0"])
        self.assertIn("mais de um assunto", out)
        self.assertIn("Código: 9", out)

    def test_troca_para_modelo_1(self):
        code, out, _ = rodar(["3", "1", "2", "1", "2", "n", "0", "0", "0"])
        self.assertIn("Formato alterado", out)
        self.assertNotIn("EM RESUMO", out)
        self.assertIn("Fonte:", out)

    def test_modo_direto_linha_de_comando(self):
        code, out, _ = rodar("", "--buscar", "cartão do sus")
        self.assertEqual(code, 0)
        self.assertIn("Código: 11", out)
        code, out, _ = rodar("", "--id", "5", "--modelo", "2")
        self.assertIn("EM RESUMO", out)
        code, out, _ = rodar("", "--id", "abc")
        self.assertEqual(code, 1)
        code, out, _ = rodar("", "--buscar", "receita de bolo")
        self.assertEqual(code, 1)
        self.assertIn("Não encontrei", out)

    def test_base_real_abre(self):
        code, out, err = rodar(["0"], base=None)
        self.assertEqual(code, 0, err)


class TestEntradasEstranhas(unittest.TestCase):
    ESTRANHAS = [
        "", " ", "\t", "    ", "0.5", "-1", "99", "1e9", "²", "١", "s", "S", "sim",
        "a" * 5000, "🙂🙂🙂", "'; DROP TABLE registros; --", "%s %d {0} {}",
        "\\n\\t", "<script>alert(1)</script>", "NULL", "None", "../../etc/passwd",
        "\x00\x00", "ç~´`^", "CPF" * 300,
    ]

    def _sem_erro(self, entradas):
        code, out, err = rodar(entradas)
        self.assertNotIn("Traceback", out + err)
        self.assertEqual(code, 0, err)
        return out

    def test_menu_principal(self):
        out = self._sem_erro(self.ESTRANHAS + ["0"])
        self.assertIn("Você não digitou nada", out)
        self.assertIn("Opção inválida", out)

    def test_busca_palavra_chave(self):
        self._sem_erro(["1"] + self.ESTRANHAS + ["0", "0"])

    def test_menu_temas_e_assuntos(self):
        self._sem_erro(["2"] + self.ESTRANHAS + ["1"] + self.ESTRANHAS + ["0", "0", "0"])

    def test_desempate(self):
        self._sem_erro(["1", "cancelar compra"] + self.ESTRANHAS + ["0", "0", "0"])

    def test_navegacao_relacionados(self):
        self._sem_erro(["1", "perdi meu cpf", "s"] + self.ESTRANHAS + ["0", "0", "0"])

    def test_troca_de_modelo(self):
        self._sem_erro(["3", "", "3", "abc", "3", "9", "0"])

    def test_entrada_muito_longa_avisa(self):
        out = self._sem_erro(["1", "cpf " * 100, "n", "0", "0"])
        self.assertIn("muito longa", out)

    def test_ctrl_d_no_meio(self):
        for entradas in ["", "1", "1\nperdi meu cpf", "1\nperdi meu cpf\ns", "2\n1", "1\ncancelar compra"]:
            code, out, err = rodar(entradas)
            self.assertNotIn("Traceback", out + err, entradas)
            self.assertEqual(code, 0, entradas)

    def test_base_quebrada_mensagem_amigavel(self):
        code, out, err = rodar(["0"], base=RAIZ / "README.md")
        self.assertEqual(code, 2)
        self.assertIn("Erro ao carregar a base", err)
        self.assertNotIn("Traceback", err)


if __name__ == "__main__":
    unittest.main()
