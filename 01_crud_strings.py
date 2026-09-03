"""
01_crud_strings.py
===================
CRUD completo utilizando o tipo de dado mais simples do Redis: STRING.

Conceitos praticados: SET, GET, MSET, MGET, EX (TTL), INCR, APPEND, DEL.
"""

import time
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def create():
    print("\n--- CREATE ---")
    r.set("produto:1", "Notebook Gamer")
    r.set("produto:2", "Mouse sem fio")
    # CREATE com expiração (TTL) de 10 segundos
    r.set("promocao:relampago", "20% OFF", ex=10)
    # Criando várias chaves de uma vez
    r.mset({"produto:3": "Teclado mecânico", "produto:4": "Monitor 24\""})
    print("Chaves criadas: produto:1, produto:2, produto:3, produto:4, promocao:relampago")


def read():
    print("\n--- READ ---")
    print("produto:1 ->", r.get("produto:1"))
    print("produto:2 ->", r.get("produto:2"))

    # Lendo várias chaves de uma vez (mais eficiente que vários GETs)
    valores = r.mget(["produto:1", "produto:2", "produto:3"])
    print("Leitura múltipla (mget):", valores)

    # Verificando o tempo de vida restante da promoção
    ttl = r.ttl("promocao:relampago")
    print(f"TTL da promoção: {ttl} segundos restantes")

    # Verificando se uma chave existe
    print("Existe produto:99?", bool(r.exists("produto:99")))


def update():
    print("\n--- UPDATE ---")
    # UPDATE simples: SET sobrescreve
    r.set("produto:1", "Notebook Gamer RTX 4060")
    print("produto:1 atualizado ->", r.get("produto:1"))

    # UPDATE numérico atômico (ótimo para contadores)
    r.set("visitas:produto:1", 0)
    for _ in range(5):
        r.incr("visitas:produto:1")
    print("Total de visitas:", r.get("visitas:produto:1"))

    # APPEND: concatena texto ao final do valor existente
    r.append("produto:1", " - Edição Especial")
    print("produto:1 após append ->", r.get("produto:1"))


def delete():
    print("\n--- DELETE ---")
    r.delete("produto:4")
    print("produto:4 removido. Existe ainda?", bool(r.exists("produto:4")))

    # Esperando a promoção expirar sozinha (demonstração do TTL)
    print("Aguardando expiração automática da chave 'promocao:relampago' (11s)...")
    time.sleep(11)
    print("promocao:relampago após expirar ->", r.get("promocao:relampago"))  # None


if __name__ == "__main__":
    create()
    read()
    update()
    delete()
