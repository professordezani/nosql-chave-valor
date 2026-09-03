"""
02_crud_hashes.py
==================
CRUD utilizando HASH - a estrutura ideal para representar um "registro"
(como uma linha de tabela em um banco relacional), agrupando vários campos
sob uma única chave.

Conceitos praticados: HSET, HGET, HGETALL, HDEL, HINCRBY, HEXISTS.
"""

import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def create():
    print("\n--- CREATE ---")
    r.hset("usuario:1", mapping={
        "nome": "Ana Souza",
        "email": "ana.souza@exemplo.com",
        "idade": 22,
        "cidade": "São José do Rio Preto",
    })
    print("Hash 'usuario:1' criado.")


def read():
    print("\n--- READ ---")
    # Lendo um campo específico (equivalente a SELECT nome FROM usuario WHERE id=1)
    nome = r.hget("usuario:1", "nome")
    print("Nome:", nome)

    # Lendo todos os campos (equivalente a SELECT * FROM usuario WHERE id=1)
    usuario = r.hgetall("usuario:1")
    print("Registro completo:", usuario)

    # Verificando se um campo existe
    print("Possui campo 'telefone'?", r.hexists("usuario:1", "telefone"))

    # Contando quantos campos o hash possui
    print("Quantidade de campos:", r.hlen("usuario:1"))


def update():
    print("\n--- UPDATE ---")
    # Atualiza um campo específico sem afetar os demais
    r.hset("usuario:1", "cidade", "Rio Preto")
    print("Cidade atualizada ->", r.hget("usuario:1", "cidade"))

    # Incrementa um campo numérico atomicamente (fez aniversário!)
    nova_idade = r.hincrby("usuario:1", "idade", 1)
    print("Nova idade após aniversário:", nova_idade)


def delete():
    print("\n--- DELETE ---")
    # Remove apenas um campo
    r.hdel("usuario:1", "email")
    print("Após remover 'email':", r.hgetall("usuario:1"))

    # Remove o hash inteiro (equivalente a DELETE FROM usuario WHERE id=1)
    r.delete("usuario:1")
    print("Usuário removido por completo. Existe ainda?", bool(r.exists("usuario:1")))


if __name__ == "__main__":
    create()
    read()
    update()
    delete()
