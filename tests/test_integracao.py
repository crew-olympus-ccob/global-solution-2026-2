import os
import subprocess
import sys
import unittest
from pathlib import Path

RAIZ = Path(__file__).resolve().parent.parent
SISTEMA = RAIZ / "src" / "sistema.py"
INDICADOR = RAIZ / "src" / "indicador.py"

ESTRANHAS = [
    "", " ", "\t", "0.5", "-1", "99", "1e9", "²", "١", "s", "abc",
    "a" * 5000, "\U0001F642" * 3, "'; DROP TABLE registros; --", "%s %d {0} {}",
    "<script>alert(1)</script>", "None", "../../etc/passwd", "\x00\x00", "ç~´`^",
]


def rodar(script, entrada="", *args, timeout=15):
    env = dict(os.environ, PYTHONIOENCODING="utf-8")
    p = subprocess.run([sys.executable, str(script), *args], input=entrada, capture_output=True,
                       text=True, encoding="utf-8", timeout=timeout, env=env, cwd=str(RAIZ))
    return p.returncode, p.stdout, p.stderr


class TestIndicadorNoTerminal(unittest.TestCase):
    def test_roda_e_mostra_a_taxa(self):
        code, out, err = rodar(INDICADOR)
        self.assertNotIn("Traceback", out + err)
        self.assertIn("Taxa de acerto geral", out)

    def test_base_inexistente_mensagem_amigavel(self):
        code, out, err = rodar(INDICADOR, "", "--base", "nao_existe.json")
        self.assertEqual(code, 2)
        self.assertNotIn("Traceback", err)


@unittest.skipUnless(SISTEMA.is_file(), "aguardando src/sistema.py (menu em loop)")
class TestSistemaNoTerminal(unittest.TestCase):
    def _sem_traceback(self, linhas):
        texto = "\n".join(linhas) + "\n"
        try:
            code, out, err = rodar(SISTEMA, texto)
        except subprocess.TimeoutExpired:
            self.fail("o programa não terminou: provável loop sem fim ao acabar a entrada")
        self.assertNotIn("Traceback", out + err)
        return out

    def test_abre_e_fecha(self):
        self._sem_traceback([])

    def test_entradas_estranhas_no_menu(self):
        self._sem_traceback(ESTRANHAS)

    def test_busca_por_pergunta_com_entradas_estranhas(self):
        self._sem_traceback(["1"] + ESTRANHAS)

    def test_busca_por_tema_com_entradas_estranhas(self):
        self._sem_traceback(["2"] + ESTRANHAS)


if __name__ == "__main__":
    unittest.main()
