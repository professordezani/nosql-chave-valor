"""
notificacoes.py  (módulo OPCIONAL / BÔNUS)
=============================================
Publica notificações em tempo real quando um novo produto é cadastrado,
usando Pub/Sub. Para ver as notificações chegando, rode em um terminal
separado:

    python -c "from notificacoes import assinar_novidades; assinar_novidades()"

...enquanto cadastra produtos em outro terminal.

Complete as funções marcadas com # TODO.
"""

from conexao import r

CANAL_NOVIDADES = "canal:novidades"


def publicar_novo_produto(nome_produto: str) -> None:
    """Publica uma notificação de novo produto cadastrado."""
    # TODO: usar r.publish(CANAL_NOVIDADES, mensagem)
    pass


def assinar_novidades() -> None:
    """Fica escutando o canal de novidades e imprime cada mensagem recebida."""
    # TODO: 1) pubsub = r.pubsub()
    #       2) pubsub.subscribe(CANAL_NOVIDADES)
    #       3) for mensagem in pubsub.listen(): ... imprimir se type == "message"
    pass
