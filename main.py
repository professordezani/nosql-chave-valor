"""
main.py
========
Menu de linha de comando (CLI) do mini-projeto de e-commerce com Redis.

Este arquivo já está funcional na sua ESTRUTURA (menu, leitura de opções),
mas depende das funções que você vai implementar em catalogo.py, carrinho.py,
pedidos.py e seguranca.py (marcadas com # TODO nesses arquivos).
"""

from conexao import testar_conexao
import catalogo
import carrinho
import pedidos
import seguranca

USUARIO_ATUAL = 1  # simplificação: sistema single-user para fins didáticos


def menu():
    print("""
========================================
   E-COMMERCE SIMPLIFICADO COM REDIS
========================================
1. Cadastrar produto
2. Listar produtos
3. Ver produto (e contar visualização)
4. Adicionar produto ao carrinho
5. Ver carrinho
6. Finalizar compra (checkout)
7. Processar próximo pedido da fila
8. Ver ranking de mais vendidos
0. Sair
""")


def acao_cadastrar_produto():
    produto_id = int(input("ID do produto: "))
    nome = input("Nome: ")
    preco = float(input("Preço: "))
    estoque = int(input("Estoque: "))
    catalogo.cadastrar_produto(produto_id, nome, preco, estoque)
    print("✅ Produto cadastrado!")


def acao_listar_produtos():
    produtos = catalogo.listar_produtos() or []
    if not produtos:
        print("Nenhum produto cadastrado ainda.")
    for p in produtos:
        print(p)


def acao_ver_produto():
    produto_id = int(input("ID do produto: "))

    if not seguranca.dentro_do_limite(USUARIO_ATUAL):
        print("🚫 Limite de consultas excedido. Tente novamente em instantes.")
        return

    produto = catalogo.consultar_produto(produto_id)
    print(produto if produto else "Produto não encontrado.")


def acao_adicionar_carrinho():
    produto_id = int(input("ID do produto: "))
    quantidade = int(input("Quantidade: "))
    carrinho.adicionar_ao_carrinho(USUARIO_ATUAL, produto_id, quantidade)
    print("✅ Produto adicionado ao carrinho!")


def acao_ver_carrinho():
    print(carrinho.ver_carrinho(USUARIO_ATUAL))


def acao_finalizar_compra():
    itens = carrinho.ver_carrinho(USUARIO_ATUAL)
    if not itens:
        print("Carrinho vazio.")
        return
    pedidos.finalizar_compra(USUARIO_ATUAL, itens)
    carrinho.esvaziar_carrinho(USUARIO_ATUAL)
    print("✅ Compra finalizada! Pedido enviado para a fila de processamento.")


def acao_processar_pedido():
    pedido = pedidos.processar_proximo_pedido(timeout=3)
    print(pedido if pedido else "Nenhum pedido pendente na fila.")


def acao_ranking():
    top = pedidos.top_produtos_mais_vendidos(5) or []
    for posicao, (produto_id, pontos) in enumerate(top, start=1):
        print(f"{posicao}º lugar: produto {produto_id} - {int(pontos)} unidades vendidas")


def main():
    if not testar_conexao():
        return

    acoes = {
        "1": acao_cadastrar_produto,
        "2": acao_listar_produtos,
        "3": acao_ver_produto,
        "4": acao_adicionar_carrinho,
        "5": acao_ver_carrinho,
        "6": acao_finalizar_compra,
        "7": acao_processar_pedido,
        "8": acao_ranking,
    }

    while True:
        menu()
        opcao = input("Escolha uma opção: ").strip()
        if opcao == "0":
            print("Até mais!")
            break
        acao = acoes.get(opcao)
        if acao:
            try:
                acao()
            except Exception as e:
                print(f"⚠️ Ocorreu um erro: {e}")
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    main()
