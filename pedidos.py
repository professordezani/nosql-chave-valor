"""
pedidos.py
===========
Módulo responsável por:
  1) Enfileirar pedidos para processamento assíncrono (List + BRPOP).
  2) Atualizar o ranking de produtos mais vendidos (Sorted Set).

Complete as funções marcadas com # TODO.
"""

import json
import time
from conexao import r

FILA_PEDIDOS = "fila:pedidos"
RANKING_MAIS_VENDIDOS = "ranking:mais_vendidos"


def finalizar_compra(usuario_id: int, itens: dict) -> None:
    """
    itens: dicionário no formato {produto_id: quantidade}

    Esta função deve:
      1) Criar um "pedido" (dict com usuario_id, itens e timestamp) e
         inserir na fila FILA_PEDIDOS como JSON (LPUSH).
      2) Para cada item comprado, incrementar sua pontuação no
         RANKING_MAIS_VENDIDOS com ZINCRBY (pontuação = quantidade comprada).
    """
    # TODO: montar o dicionário do pedido
    # TODO: r.lpush(FILA_PEDIDOS, json.dumps(pedido))
    # TODO: para cada produto_id, quantidade em itens.items(): r.zincrby(...)
    pass


def processar_proximo_pedido(timeout: int = 5) -> dict | None:
    """
    Consome (remove) o próximo pedido da fila, simulando o processamento
    (ex.: separação, embalagem, envio). Retorna o pedido processado ou
    None se não houver pedidos dentro do timeout.
    """
    # TODO: usar r.brpop(FILA_PEDIDOS, timeout=timeout)
    #       lembrar que brpop retorna uma tupla (chave, valor) ou None
    pass


def top_produtos_mais_vendidos(quantidade: int = 5) -> list[tuple[str, float]]:
    """Retorna os produtos mais vendidos, do maior para o menor."""
    # TODO: usar r.zrevrange(RANKING_MAIS_VENDIDOS, 0, quantidade - 1, withscores=True)
    pass
