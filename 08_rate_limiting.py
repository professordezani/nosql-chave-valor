"""
08_rate_limiting.py
=====================
Implementa um limitador de requisições (rate limiter) de "janela fixa"
usando apenas INCR + EXPIRE — um padrão extremamente comum para proteger
APIs contra abuso.

Conceitos praticados: INCR (atômico), EXPIRE, simulação de requisições.
"""

import time
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


def permitir_requisicao(identificador: str, limite: int = 5, janela_segundos: int = 10) -> bool:
    """
    Retorna True se a requisição pode prosseguir, False se o limite foi excedido.

    identificador: pode ser um IP, um usuário, uma API key, etc.
    limite: quantas requisições são permitidas por janela de tempo.
    janela_segundos: duração da janela de tempo.
    """
    chave = f"rate_limit:{identificador}"

    total_requisicoes = r.incr(chave)

    # Se essa foi a primeira requisição da janela, define quando ela expira
    if total_requisicoes == 1:
        r.expire(chave, janela_segundos)

    if total_requisicoes > limite:
        ttl_restante = r.ttl(chave)
        print(f"🚫 Requisição #{total_requisicoes} BLOQUEADA. "
              f"Tente novamente em {ttl_restante}s. (limite: {limite}/{janela_segundos}s)")
        return False

    print(f"✅ Requisição #{total_requisicoes} permitida. (limite: {limite}/{janela_segundos}s)")
    return True


if __name__ == "__main__":
    ip_cliente = "200.150.10.5"

    print("Simulando 8 requisições rápidas de um mesmo IP (limite = 5 a cada 10s):\n")
    for i in range(8):
        permitir_requisicao(ip_cliente, limite=5, janela_segundos=10)
        time.sleep(0.3)  # requisições quase simultâneas

    print("\nAguardando a janela expirar (11s) para o limite resetar...")
    time.sleep(11)

    print("\nNova rodada após a janela expirar:")
    permitir_requisicao(ip_cliente, limite=5, janela_segundos=10)
