"""
carrinho.py
============
Módulo responsável pelo carrinho de compras de cada usuário.

Sugestão de estrutura: um HASH por usuário, onde cada campo é o produto_id
e o valor é a quantidade desejada. O carrinho expira automaticamente após
um período de inatividade (TTL), simulando o comportamento comum de
e-commerces reais.

Complete as funções marcadas com # TODO.
"""

from conexao import r

TTL_CARRINHO_SEGUNDOS = 30 * 60  # 30 minutos


def _chave_carrinho(usuario_id: int) -> str:
    return f"carrinho:{usuario_id}"


def adicionar_ao_carrinho(usuario_id: int, produto_id: int, quantidade: int = 1) -> None:
    """Adiciona um produto ao carrinho (ou aumenta a quantidade, se já existir)."""
    chave = _chave_carrinho(usuario_id)
    # TODO: 1) usar HINCRBY para somar a quantidade ao campo do produto
    #       2) renovar o TTL do carrinho com EXPIRE a cada alteração
    pass


def remover_do_carrinho(usuario_id: int, produto_id: int) -> None:
    """Remove um produto do carrinho."""
    # TODO: usar HDEL
    pass


def ver_carrinho(usuario_id: int) -> dict:
    """Retorna o conteúdo atual do carrinho: {produto_id: quantidade}."""
    # TODO: usar HGETALL
    pass


def esvaziar_carrinho(usuario_id: int) -> None:
    """Remove o carrinho inteiro (ex.: após finalizar a compra)."""
    # TODO: usar DELETE
    pass
