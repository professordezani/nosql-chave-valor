"""
seguranca.py
=============
Módulo responsável pelo rate limiting das consultas de produto, evitando
que um único usuário sobrecarregue o sistema com requisições excessivas.

Reaproveite a lógica vista em aula (INCR + EXPIRE, janela fixa).

Complete a função marcada com # TODO.
"""

from conexao import r


def dentro_do_limite(usuario_id: int, limite: int = 20, janela_segundos: int = 60) -> bool:
    """
    Retorna True se o usuário ainda pode realizar a operação,
    False se o limite de requisições na janela de tempo foi excedido.
    """
    # TODO: 1) montar a chave, ex.: f"rate_limit:usuario:{usuario_id}"
    #       2) incrementar com INCR
    #       3) se for a primeira requisição da janela (total == 1), definir EXPIRE
    #       4) retornar total <= limite
    pass
