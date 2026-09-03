"""
00_conexao.py
=============
Primeiro contato com o Redis a partir do Python.

Como executar:
- VSCode (local): rode um Redis com Docker antes:
    docker run -d --name redis-aula -p 6379:6379 redis:7-alpine
- Google Colab: não existe Redis local no Colab. Crie um banco gratuito em
    https://redis.io/try-free e troque HOST / PORT / SENHA abaixo.

Instalação da biblioteca (uma vez só):
    pip install redis
"""

import redis

# ---------------------------------------------------------------------------
# CONFIGURAÇÃO DA CONEXÃO
# ---------------------------------------------------------------------------
# Opção A) Redis local (Docker/VSCode) -> deixe como está
HOST = "localhost"
PORT = 6379
PASSWORD = None

# Opção B) Redis Cloud (necessário para Google Colab) -> descomente e preencha
# HOST = "redis-XXXXX.c.redis-cloud.com"
# PORT = 17845
# PASSWORD = "sua_senha_aqui"

r = redis.Redis(
    host=HOST,
    port=PORT,
    password=PASSWORD,
    decode_responses=True,  # importante: devolve str em vez de bytes
)


def main():
    # 1) Testando a conexão
    print("Ping:", r.ping())  # True se conectou com sucesso

    # 2) Informações básicas do servidor
    info = r.info("server")
    print("Versão do Redis:", info.get("redis_version"))

    # 3) Primeira escrita e leitura
    r.set("aula", "banco de dados chave-valor")
    valor = r.get("aula")
    print("Valor lido:", valor)

    # 4) Quantas chaves existem no banco atual?
    print("Total de chaves no banco:", r.dbsize())


if __name__ == "__main__":
    main()
