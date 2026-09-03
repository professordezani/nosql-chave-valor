# Mini-Projeto — Sistema de E-commerce Simplificado com Redis

**Disciplina:** Banco de Dados Não Relacional
**Curso:** Análise e Desenvolvimento de Sistemas — 3º semestre
**Tecnologias:** Python 3.10+ e Redis (via `redis-py`)
**Modalidade:** Individual ou em dupla (definir com o professor)

---

## 1. Objetivo

Construir, em Python, um sistema simplificado de e-commerce que utilize o Redis
como banco de dados principal, aplicando na prática os conceitos vistos em
aula: estruturas de dados do Redis, CRUD, TTL, filas, Pub/Sub, rate limiting
e rankings.

O projeto **não** precisa ter interface gráfica. Uma interface de linha de
comando (CLI) com um menu simples já atende aos requisitos.

---

## 2. Requisitos Funcionais

O sistema deve implementar os módulos abaixo. Cada módulo indica a estrutura
de dados do Redis sugerida — o uso de outra estrutura é permitido, desde que
justificado no relatório final.

### 2.1. Catálogo de Produtos — `Hash`
- [ ] Cadastrar um produto (`id`, `nome`, `preco`, `estoque`).
- [ ] Consultar um produto pelo `id`.
- [ ] Atualizar preço e/ou estoque de um produto.
- [ ] Remover um produto.
- [ ] Listar todos os produtos cadastrados (dica: mantenha um `Set` auxiliar
      com todos os IDs de produtos, ex.: `produtos:ids`, já que o Redis não
      lista hashes por padrão).

### 2.2. Carrinho de Compras — `Hash` ou `List` + `TTL`
- [ ] Adicionar um produto ao carrinho de um usuário (`carrinho:<usuario_id>`).
- [ ] Remover um produto do carrinho.
- [ ] Consultar o conteúdo atual do carrinho.
- [ ] O carrinho deve expirar automaticamente após um período de inatividade
      (ex.: 30 minutos) — utilize `EXPIRE`.

### 2.3. Contador de Visualizações — `String` + `INCR`
- [ ] Toda vez que um produto for consultado (`ver_produto`), incrementar um
      contador `visualizacoes:<produto_id>`.
- [ ] Exibir o número de visualizações de um produto junto aos seus dados.

### 2.4. Ranking de Mais Vendidos — `Sorted Set`
- [ ] Ao finalizar uma compra (checkout), incrementar a pontuação do produto
      no ranking `ranking:mais_vendidos` com a quantidade vendida.
- [ ] Implementar uma função que retorne o Top N produtos mais vendidos.

### 2.5. Fila de Processamento de Pedidos — `List` + `BRPOP`
- [ ] Ao finalizar uma compra, um "pedido" (JSON serializado) deve ser
      inserido na fila `fila:pedidos`.
- [ ] Implementar um processo consumidor (pode ser uma função chamada
      manualmente ou um script separado) que processa os pedidos da fila
      em ordem (FIFO), simulando o envio ao cliente.

### 2.6. Rate Limiting — `INCR` + `EXPIRE`
- [ ] Implementar um limite de "requisições" nas funções de consulta de
      produto (ex.: no máximo 20 consultas por usuário a cada 60 segundos).
      Se o limite for excedido, a função deve recusar a operação com uma
      mensagem apropriada.

### 2.7. (Opcional/Bônus) Notificações em Tempo Real — `Pub/Sub`
- [ ] Ao cadastrar um novo produto, publicar uma notificação no canal
      `canal:novidades`.
- [ ] Implementar um "assinante" simples que imprime as notificações
      recebidas (pode ser executado em um terminal separado).

---

## 3. Requisitos Técnicos

- O código deve estar organizado (sugestão de estrutura na seção 5).
- Utilizar `redis-py` com `decode_responses=True`.
- Tratar exceções de conexão (`redis.exceptions.ConnectionError`, etc.).
- Utilizar nomes de chave padronizados com `:` (ex.: `produto:10`,
  `carrinho:usuario:5`), conforme boas práticas vistas em aula.
- Não é necessário banco relacional — o Redis é a única fonte de dados
  deste mini-projeto (na vida real, ele seria complementar a um SQL Server,
  mas aqui o objetivo é fixar o uso do Redis isoladamente).

---

## 4. Como Executar

1. Suba um Redis local (Docker) ou crie um banco gratuito no Redis Cloud:
   ```bash
   docker run -d --name redis-projeto -p 6379:6379 redis:7-alpine
   ```
2. Instale as dependências:
   ```bash
   pip install redis
   ```
3. Execute o menu principal:
   ```bash
   python main.py
   ```

Um template inicial de projeto está disponível na pasta `templates/` deste
mesmo diretório, com a estrutura de pastas, um menu de CLI básico e as
assinaturas de função já esboçadas (`# TODO`) para você completar.

---

## 5. Estrutura de Pastas Sugerida

```
mini_projeto_ecommerce/
├── main.py                # menu / CLI principal
├── conexao.py             # configuração da conexão com o Redis
├── catalogo.py            # funções do catálogo de produtos (Hash)
├── carrinho.py            # funções do carrinho de compras
├── pedidos.py             # fila de pedidos + ranking de mais vendidos
├── seguranca.py           # rate limiting
└── notificacoes.py        # (opcional) Pub/Sub
```

---

## 6. Critérios de Avaliação

| Critério | Peso |
|---|---|
| Catálogo de produtos (CRUD completo) | 20% |
| Carrinho de compras com TTL | 15% |
| Contador de visualizações | 10% |
| Ranking de mais vendidos (Sorted Set) | 15% |
| Fila de processamento de pedidos | 15% |
| Rate limiting | 15% |
| Organização do código e boas práticas de nomenclatura de chaves | 10% |
| **Bônus:** Pub/Sub de notificações | +10% |

---

## 7. Perguntas para o Relatório Final (entregar junto ao código)

1. Quais estruturas de dados do Redis você utilizou em cada módulo e por quê?
2. Se este sistema fosse para produção, você manteria o Redis como única
   fonte de dados ou o combinaria com um banco relacional (ex.: SQL Server)?
   Justifique tecnicamente usando o Teorema CAP.
3. Qual foi a maior dificuldade técnica enfrentada e como você resolveu?
4. O que aconteceria com os dados do seu carrinho de compras se o servidor
   Redis reiniciasse sem persistência (RDB/AOF) configurada? Isso é aceitável
   para este caso de uso? Justifique.
