"""
catalogo.py
============
Módulo responsável pelo CRUD de produtos, usando HASH para cada produto
e um SET auxiliar (`produtos:ids`) para permitir listar todos os produtos
cadastrados (o Redis não lista hashes automaticamente).

Complete as funções marcadas com # TODO.
"""

from conexao import r

CHAVE_IDS = "produtos:ids"


def _chave_produto(produto_id: int) -> str:
    return f"produto:{produto_id}"


def cadastrar_produto(produto_id: int, nome: str, preco: float, estoque: int) -> None:
    """Cria (ou sobrescreve) um produto no catálogo."""
    # TODO: 1) usar HSET para salvar os campos nome, preco e estoque
    #       2) usar SADD para adicionar produto_id ao conjunto CHAVE_IDS
    pass


def consultar_produto(produto_id: int) -> dict | None:
    """Retorna os dados de um produto e incrementa seu contador de visualizações."""
    chave = _chave_produto(produto_id)

    # TODO: verificar se o produto existe (HGETALL retorna {} se não existir)
    # TODO: incrementar r.incr(f"visualizacoes:{produto_id}")
    # TODO: retornar um dicionário com os dados do produto + total de visualizações
    pass


def atualizar_estoque(produto_id: int, nova_quantidade: int) -> None:
    """Atualiza apenas o campo de estoque de um produto."""
    # TODO: usar HSET para atualizar somente o campo "estoque"
    pass


def atualizar_preco(produto_id: int, novo_preco: float) -> None:
    """Atualiza apenas o campo de preço de um produto."""
    # TODO
    pass


def remover_produto(produto_id: int) -> None:
    """Remove um produto do catálogo por completo."""
    # TODO: 1) DEL na chave do hash do produto
    #       2) SREM para remover o produto_id do conjunto CHAVE_IDS
    pass


def listar_produtos() -> list[dict]:
    """Retorna uma lista com os dados de todos os produtos cadastrados."""
    # TODO: 1) obter todos os IDs com SMEMBERS(CHAVE_IDS)
    #       2) para cada ID, buscar o hash correspondente com HGETALL
    #       3) retornar a lista de dicionários
    pass
