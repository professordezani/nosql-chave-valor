"""
05_cache_aside.py
===================
Demonstra o padrão CACHE-ASIDE: a aplicação sempre consulta o Redis primeiro;
se não encontrar (cache miss), busca na "fonte da verdade" (aqui simulada por
um dicionário Python, no lugar do SQL Server) e grava o resultado no Redis
com um TTL antes de devolver ao usuário.

Conceitos praticados: GET, SETEX (SET com EX), medição de latência,
                       cache hit vs cache miss.
"""

import time
import json
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

TTL_CACHE_SEGUNDOS = 30

# ---------------------------------------------------------------------------
# Simulação de um banco relacional "lento" (ex.: SQL Server)
# ---------------------------------------------------------------------------
BANCO_RELACIONAL = {
    1: {"id": 1, "nome": "Notebook Gamer", "preco": 5999.90, "estoque": 12},
    2: {"id": 2, "nome": "Mouse sem fio", "preco": 89.90, "estoque": 150},
    3: {"id": 3, "nome": "Teclado mecânico", "preco": 349.90, "estoque": 40},
}


def consultar_banco_relacional(produto_id: int) -> dict | None:
    """Simula uma consulta 'cara' ao banco relacional (latência artificial)."""
    time.sleep(1.2)  # simula tempo de disco/rede/índice
    return BANCO_RELACIONAL.get(produto_id)


def buscar_produto(produto_id: int) -> dict | None:
    """Implementa o padrão cache-aside."""
    chave_cache = f"cache:produto:{produto_id}"

    # 1) Tenta buscar no Redis primeiro
    inicio = time.time()
    dado_em_cache = r.get(chave_cache)

    if dado_em_cache:
        duracao = (time.time() - inicio) * 1000
        print(f"✅ CACHE HIT  ({duracao:.2f} ms) -> produto {produto_id}")
        return json.loads(dado_em_cache)

    # 2) Cache miss: consulta a fonte da verdade
    print(f"❌ CACHE MISS -> consultando o banco relacional para o produto {produto_id}...")
    produto = consultar_banco_relacional(produto_id)

    if produto is None:
        return None

    # 3) Grava no cache com TTL antes de retornar
    r.set(chave_cache, json.dumps(produto), ex=TTL_CACHE_SEGUNDOS)
    duracao = (time.time() - inicio) * 1000
    print(f"🐢 Consulta ao banco relacional levou {duracao:.2f} ms (e agora está em cache por {TTL_CACHE_SEGUNDOS}s)")
    return produto


if __name__ == "__main__":
    print("1ª chamada — deve dar CACHE MISS:")
    print(buscar_produto(1))

    print("\n2ª chamada (mesmo produto) — deve dar CACHE HIT e ser muito mais rápida:")
    print(buscar_produto(1))

    print("\n3ª chamada — produto diferente, novo CACHE MISS:")
    print(buscar_produto(2))

    print(f"\nAguardando {TTL_CACHE_SEGUNDOS}s para o cache expirar...")
    time.sleep(TTL_CACHE_SEGUNDOS + 1)

    print("\n4ª chamada, após expiração — CACHE MISS novamente:")
    print(buscar_produto(1))
