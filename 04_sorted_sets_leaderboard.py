"""
04_sorted_sets_leaderboard.py
================================
Sorted Sets (ZSET) são a estrutura perfeita para RANKINGS: cada membro tem
uma pontuação (score) e o Redis mantém tudo ordenado automaticamente,
sem que a aplicação precise reordenar nada.

Conceitos praticados: ZADD, ZRANGE, ZREVRANGE, ZSCORE, ZINCRBY,
                       ZRANK/ZREVRANK, ZREM.
"""

import redis

r = redis.Redis(host="localhost", port=6379, decode_responses=True)

RANKING = "ranking:jogo1"


def criar_ranking_inicial():
    print("\n--- CREATE ---")
    r.delete(RANKING)
    r.zadd(RANKING, {
        "ana": 1500,
        "leo": 2100,
        "carla": 1800,
        "davi": 950,
    })
    print("Ranking inicial criado com 4 jogadores.")


def consultar_ranking():
    print("\n--- READ ---")
    # Top 3 jogadores, do maior para o menor score, com pontuação
    top3 = r.zrevrange(RANKING, 0, 2, withscores=True)
    print("🏆 Top 3 jogadores:")
    for posicao, (jogador, pontos) in enumerate(top3, start=1):
        print(f"   {posicao}º lugar: {jogador} - {int(pontos)} pontos")

    # Pontuação de um jogador específico
    print("\nPontuação da Ana:", r.zscore(RANKING, "ana"))

    # Posição (rank) de um jogador específico (0 = melhor colocado)
    posicao_leo = r.zrevrank(RANKING, "leo")
    print(f"Posição do Leo no ranking: {posicao_leo + 1}º lugar")


def atualizar_pontuacao():
    print("\n--- UPDATE ---")
    # Jogador pontuou mais 300 pontos em uma partida
    novo_total = r.zincrby(RANKING, 300, "davi")
    print(f"Davi pontuou! Novo total: {int(novo_total)} pontos")

    print("Ranking atualizado:")
    for jogador, pontos in r.zrevrange(RANKING, 0, -1, withscores=True):
        print(f"   {jogador}: {int(pontos)} pontos")


def remover_jogador():
    print("\n--- DELETE ---")
    r.zrem(RANKING, "carla")
    print("Carla removida do ranking (ex.: encerrou a conta).")
    print("Ranking final:", r.zrevrange(RANKING, 0, -1, withscores=True))


if __name__ == "__main__":
    criar_ranking_inicial()
    consultar_ranking()
    atualizar_pontuacao()
    remover_jogador()
