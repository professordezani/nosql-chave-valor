"""
conexao.py
===========
Configuração centralizada da conexão com o Redis para o mini-projeto.

Todos os outros módulos devem importar a variável `r` daqui, em vez de
criar suas próprias conexões — isso evita desperdício de conexões abertas.
"""

import redis

# ---------------------------------------------------------------------------
# Ajuste estes dados conforme seu ambiente:
#   - VSCode + Docker local -> mantenha host="localhost"
#   - Google Colab -> preencha com os dados do seu banco no Redis Cloud
# ---------------------------------------------------------------------------
HOST = "localhost"
PORT = 6379
PASSWORD = None

pool = redis.ConnectionPool(
    host=HOST,
    port=PORT,
    password=PASSWORD,
    decode_responses=True,
    max_connections=20,
)

r = redis.Redis(connection_pool=pool)


def testar_conexao() -> bool:
    """Retorna True se a conexão com o Redis está funcionando."""
    try:
        return r.ping()
    except redis.exceptions.ConnectionError:
        print("❌ Não foi possível conectar ao Redis. Verifique HOST/PORT/PASSWORD.")
        return False
