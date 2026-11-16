"""Fonte e aviso compartilhados pelos modelos de resposta."""

from datetime import datetime

AVISO = (
    "Aviso: esta orientação é informativa e não oficial. "
    "Confirme as informações nos canais oficiais indicados."
)


def formatar_fonte_aviso(registro):
    """Devolve a fonte, a data de verificação e o aviso para um registro."""
    fonte = registro.get("referencia") or "Não informada"
    data = registro.get("data_verificacao")
    try:
        data = datetime.strptime(data, "%Y-%m-%d").strftime("%d/%m/%Y")
    except (TypeError, ValueError):
        data = str(data) if data else "Não informada"
    return f"Fonte: {fonte}\nVerificada em: {data}\n{AVISO}"
