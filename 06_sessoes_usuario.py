"""
06_sessoes_usuario.py
=======================
Simula um sistema de login que usa Redis para armazenar sessões de usuário,
uma das aplicações mais comuns de bancos chave-valor no mundo real.

Conceitos praticados: HSET, EXPIRE, EXISTS, TTL, geração de token,
                       renovação de sessão a cada requisição.
"""

import uuid
import time
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

DURACAO_SESSAO_SEGUNDOS = 15  # curto, só para a demonstração ser rápida


def login(usuario_id: int, nome: str) -> str:
    """Cria uma nova sessão e retorna o token gerado."""
    token = str(uuid.uuid4())
    chave = f"sessao:{token}"

    r.hset(chave, mapping={"usuario_id": usuario_id, "nome": nome})
    r.expire(chave, DURACAO_SESSAO_SEGUNDOS)

    print(f"🔓 Login efetuado para '{nome}'. Token: {token}")
    return token


def validar_sessao(token: str) -> dict | None:
    """Verifica se a sessão ainda é válida e renova o TTL (sliding expiration)."""
    chave = f"sessao:{token}"

    if not r.exists(chave):
        print("🔒 Sessão inválida ou expirada.")
        return None

    # Renova a sessão a cada requisição válida (padrão comum em apps web)
    r.expire(chave, DURACAO_SESSAO_SEGUNDOS)
    dados = r.hgetall(chave)
    print(f"✅ Sessão válida. Usuário: {dados['nome']} (TTL renovado para {DURACAO_SESSAO_SEGUNDOS}s)")
    return dados


def logout(token: str):
    """Encerra a sessão manualmente (ex.: usuário clicou em 'sair')."""
    r.delete(f"sessao:{token}")
    print("👋 Logout efetuado. Sessão removida.")


if __name__ == "__main__":
    token = login(usuario_id=42, nome="Ana Souza")

    print("\nSimulando 3 requisições válidas, uma a cada 5 segundos...")
    for _ in range(3):
        time.sleep(5)
        validar_sessao(token)

    print("\nEncerrando sessão manualmente:")
    logout(token)

    print("\nTentando validar após o logout:")
    validar_sessao(token)
