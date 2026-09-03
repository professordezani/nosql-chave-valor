"""
03_crud_listas_sets.py
========================
CRUD com LIST (filas/pilhas) e SET (coleções únicas não ordenadas).

Conceitos praticados: LPUSH, RPUSH, LRANGE, LPOP, RPOP,
                       SADD, SMEMBERS, SISMEMBER, SREM, SCARD.
"""

import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def demo_listas():
    print("\n===== LISTAS (fila de pedidos) =====")
    chave = "fila:pedidos"
    r.delete(chave)  # garante que começamos do zero

    print("\n--- CREATE ---")
    r.rpush(chave, "pedido-101", "pedido-102", "pedido-103")
    print("Pedidos inseridos (RPUSH, mantém ordem de chegada = fila FIFO)")

    print("\n--- READ ---")
    todos = r.lrange(chave, 0, -1)  # 0 até -1 = do início ao fim
    print("Todos os pedidos na fila:", todos)
    print("Tamanho da fila:", r.llen(chave))

    print("\n--- UPDATE (inserir com prioridade) ---")
    r.lpush(chave, "pedido-URGENTE")  # entra na frente da fila
    print("Fila após pedido urgente:", r.lrange(chave, 0, -1))

    print("\n--- DELETE (processar/consumir) ---")
    processado = r.lpop(chave)  # remove e retorna o primeiro da fila
    print("Pedido processado:", processado)
    print("Fila restante:", r.lrange(chave, 0, -1))


def demo_sets():
    print("\n===== SETS (tags de um post de blog) =====")
    chave = "tags:post:42"
    r.delete(chave)

    print("\n--- CREATE ---")
    r.sadd(chave, "redis", "nosql", "banco-de-dados", "redis")  # duplicata é ignorada
    print("Tags adicionadas (duplicatas são automaticamente ignoradas)")

    print("\n--- READ ---")
    print("Todas as tags:", r.smembers(chave))
    print("Total de tags únicas:", r.scard(chave))
    print("'redis' é uma tag?", bool(r.sismember(chave, "redis")))
    print("'python' é uma tag?", bool(r.sismember(chave, "python")))

    print("\n--- UPDATE (adicionar mais uma tag) ---")
    r.sadd(chave, "python")
    print("Tags após adicionar 'python':", r.smembers(chave))

    print("\n--- DELETE ---")
    r.srem(chave, "nosql")
    print("Tags após remover 'nosql':", r.smembers(chave))


if __name__ == "__main__":
    demo_listas()
    demo_sets()
