"""
07_filas_pubsub.py
====================
Demonstra as duas formas mais comuns de comunicação assíncrona com Redis:

1) FILA com Listas (LPUSH/BRPOP): mensagens PERSISTEM até serem consumidas.
   Ideal para tarefas que não podem se perder (ex.: processar um pedido).

2) PUB/SUB (PUBLISH/SUBSCRIBE): mensagens são entregues em tempo real e
   NÃO ficam armazenadas — se ninguém estiver ouvindo, a mensagem se perde.
   Ideal para notificações ao vivo.

Como executar a parte de Pub/Sub (precisa de 2 terminais):
    Terminal 1: python 07_filas_pubsub.py assinante
    Terminal 2: python 07_filas_pubsub.py publicador

Para rodar a demonstração da fila (não precisa de 2 terminais):
    python 07_filas_pubsub.py fila
"""

import sys
import time
import json
import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)


# ---------------------------------------------------------------------------
# 1) FILA (Listas) — Produtor / Consumidor
# ---------------------------------------------------------------------------
def demo_fila():
    fila = "fila:pedidos"
    r.delete(fila)

    print("--- Produtor: adicionando 3 pedidos na fila ---")
    for i in range(1, 4):
        pedido = json.dumps({"pedido_id": i, "item": f"Produto {i}"})
        r.lpush(fila, pedido)
        print(f"Pedido {i} adicionado à fila.")

    print("\n--- Consumidor: processando pedidos (FIFO) ---")
    while r.llen(fila) > 0:
        # BRPOP bloqueia até haver um item (aqui usamos timeout curto pois já sabemos que há itens)
        _, tarefa = r.brpop(fila, timeout=2)
        pedido = json.loads(tarefa)
        print(f"Processando pedido #{pedido['pedido_id']} ({pedido['item']})...")
        time.sleep(0.5)  # simula processamento

    print("\nFila vazia. Todos os pedidos foram processados!")


# ---------------------------------------------------------------------------
# 2) PUB/SUB — Publicador e Assinante
# ---------------------------------------------------------------------------
def demo_publicador():
    canal = "canal:notificacoes"
    print(f"Publicando mensagens no canal '{canal}'. Ctrl+C para parar.")
    contador = 0
    try:
        while True:
            contador += 1
            mensagem = f"Notificação #{contador}: novo evento no sistema!"
            qtd_assinantes = r.publish(canal, mensagem)
            print(f"Publicado: '{mensagem}' (recebido por {qtd_assinantes} assinante(s))")
            time.sleep(3)
    except KeyboardInterrupt:
        print("\nPublicador encerrado.")


def demo_assinante():
    canal = "canal:notificacoes"
    pubsub = r.pubsub()
    pubsub.subscribe(canal)
    print(f"Assinando o canal '{canal}'. Aguardando mensagens... (Ctrl+C para parar)")

    try:
        for mensagem in pubsub.listen():
            if mensagem["type"] == "message":
                print(f"📩 Mensagem recebida: {mensagem['data']}")
    except KeyboardInterrupt:
        print("\nAssinante encerrado.")


if __name__ == "__main__":
    modo = sys.argv[1] if len(sys.argv) > 1 else "fila"

    if modo == "fila":
        demo_fila()
    elif modo == "publicador":
        demo_publicador()
    elif modo == "assinante":
        demo_assinante()
    else:
        print("Uso: python 07_filas_pubsub.py [fila|publicador|assinante]")
