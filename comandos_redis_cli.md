# Sequências de Comandos Redis — CRUD e Aplicações

**Como usar:** copie e cole os blocos de comando, em ordem, no `redis-cli` ou no
**Workbench do RedisInsight**. Cada bloco representa um passo de uma história
contínua (a mesma chave evolui de comando para comando), então a ordem importa.

> 💡 Nas sequências abaixo, cada estrutura de dados é aplicada à entidade que
> melhor a representa: **Produto** (String, Set e Sorted Set), **Usuário**
> (Hash) e **Pedido** (List).

---

## 1. CRUD com STRING — Entidade: Produto (contador de visualizações)

**Contexto:** toda vez que a página de um produto é acessada, incrementamos um contador simples.

**1) CREATE** — cria o contador de visualizações do produto 101, começando em zero.
```
SET visualizacoes:produto:101 0
```

**2) READ** — lê o valor atual do contador.
```
GET visualizacoes:produto:101
```

**3) UPDATE** — incrementa o contador a cada nova visualização (simula 3 acessos).
```
INCR visualizacoes:produto:101
INCR visualizacoes:produto:101
INCR visualizacoes:produto:101
```

**4) READ (verificação)** — confirma que o contador acumulou os 3 acessos.
```
GET visualizacoes:produto:101
```

**5) UPDATE com TTL** — recria a chave com expiração de 60s, simulando um contador "diário" que zera sozinho.
```
SET visualizacoes:produto:101 0 EX 60
TTL visualizacoes:produto:101
```

**6) DELETE** — remove o contador manualmente (ex.: produto foi descontinuado).
```
DEL visualizacoes:produto:101
```

---

## 2. CRUD com HASH — Entidade: Usuário (perfil completo)

**Contexto:** um hash guarda todos os dados de cadastro de um usuário, como uma linha de tabela.

**1) CREATE** — cria o perfil do usuário 55 com vários campos de uma vez.
```
HSET usuario:55 nome "Ana Souza" email "ana@exemplo.com" idade 22 cidade "Rio Preto"
```

**2) READ (campo único)** — lê apenas o e-mail do usuário.
```
HGET usuario:55 email
```

**3) READ (registro completo)** — lê todos os campos do usuário, como um `SELECT *`.
```
HGETALL usuario:55
```

**4) READ (existência)** — verifica se o usuário já tem um campo "telefone" cadastrado.
```
HEXISTS usuario:55 telefone
```

**5) UPDATE (campo específico)** — atualiza a cidade do usuário, sem afetar os demais campos.
```
HSET usuario:55 cidade "São José do Rio Preto"
```

**6) UPDATE (numérico)** — incrementa a idade em 1 (fez aniversário), de forma atômica.
```
HINCRBY usuario:55 idade 1
```

**7) DELETE (campo único)** — remove apenas o campo "email" (ex.: usuário pediu para remover o contato).
```
HDEL usuario:55 email
```

**8) DELETE (registro completo)** — remove o usuário inteiro (ex.: exclusão de conta).
```
DEL usuario:55
```

---

## 3. CRUD com LIST — Entidade: Pedido (fila de processamento)

**Contexto:** pedidos entram em uma fila FIFO (primeiro a entrar, primeiro a sair) para serem processados pelo sistema de logística.

**1) CREATE** — insere 3 pedidos na fila, na ordem em que chegaram.
```
RPUSH fila:pedidos "pedido:201" "pedido:202" "pedido:203"
```

**2) READ (todos os itens)** — lista todos os pedidos atualmente na fila.
```
LRANGE fila:pedidos 0 -1
```

**3) READ (tamanho da fila)** — verifica quantos pedidos estão aguardando processamento.
```
LLEN fila:pedidos
```

**4) READ (item específico)** — consulta apenas o próximo pedido a ser processado, sem removê-lo.
```
LINDEX fila:pedidos 0
```

**5) UPDATE (prioridade)** — um pedido urgente chega e "fura a fila", entrando na frente de todos.
```
LPUSH fila:pedidos "pedido:URGENTE"
```

**6) UPDATE (substituir item)** — corrige o valor de uma posição específica da lista (ex.: pedido cancelado e substituído).
```
LSET fila:pedidos 1 "pedido:202-CANCELADO"
```

**7) DELETE (processar um item)** — remove e retorna o primeiro pedido da fila (processamento FIFO).
```
LPOP fila:pedidos
```

**8) DELETE (item específico)** — remove um pedido específico de qualquer posição da fila, pelo valor.
```
LREM fila:pedidos 1 "pedido:202-CANCELADO"
```

**9) DELETE (fila inteira)** — encerra o dia e limpa a fila por completo.
```
DEL fila:pedidos
```

---

## 4. CRUD com SET — Entidade: Produto (categorias/tags)

**Contexto:** um produto pode pertencer a várias categorias/tags, sem ordem e sem repetição.

**1) CREATE** — associa 3 tags ao produto 101.
```
SADD tags:produto:101 "eletronico" "gamer" "notebook"
```

**2) READ (todos os membros)** — lista todas as tags do produto.
```
SMEMBERS tags:produto:101
```

**3) READ (pertencimento)** — verifica se o produto tem a tag "gamer".
```
SISMEMBER tags:produto:101 "gamer"
```

**4) READ (contagem)** — conta quantas tags o produto possui.
```
SCARD tags:produto:101
```

**5) UPDATE (adicionar mais)** — adiciona a tag "promocao" (tentar adicionar "gamer" de novo seria ignorado, pois já existe).
```
SADD tags:produto:101 "promocao"
```

**6) DELETE (uma tag)** — remove a tag "promocao" ao fim da campanha.
```
SREM tags:produto:101 "promocao"
```

**7) DELETE (conjunto inteiro)** — remove todas as tags do produto (ex.: produto foi descontinuado).
```
DEL tags:produto:101
```

---

## 5. CRUD com SORTED SET — Entidade: Produto (ranking de mais vendidos)

**Contexto:** cada produto tem uma pontuação (quantidade vendida) e o Redis mantém tudo ordenado automaticamente.

**1) CREATE** — cadastra a pontuação inicial de 4 produtos no ranking.
```
ZADD ranking:mais_vendidos 120 "produto:101" 340 "produto:102" 75 "produto:103" 200 "produto:104"
```

**2) READ (top N, decrescente)** — consulta os 3 produtos mais vendidos, com suas pontuações.
```
ZREVRANGE ranking:mais_vendidos 0 2 WITHSCORES
```

**3) READ (pontuação de um item)** — consulta quantas unidades do produto 102 já foram vendidas.
```
ZSCORE ranking:mais_vendidos "produto:102"
```

**4) READ (posição no ranking)** — descobre em que posição o produto 104 está (0 = 1º lugar).
```
ZREVRANK ranking:mais_vendidos "produto:104"
```

**5) UPDATE (nova venda)** — o produto 103 vende mais 50 unidades; a pontuação é somada atomicamente.
```
ZINCRBY ranking:mais_vendidos 50 "produto:103"
```

**6) DELETE (remover item)** — remove o produto 101 do ranking (ex.: saiu de linha).
```
ZREM ranking:mais_vendidos "produto:101"
```

**7) DELETE (ranking inteiro)** — zera o ranking (ex.: início de um novo mês/campanha).
```
DEL ranking:mais_vendidos
```

---

# Comandos por Aplicação

## Aplicação 1 — Cache-Aside (Produto)

**Contexto:** a aplicação consulta o cache antes de ir ao banco relacional. Aqui simulamos manualmente o comportamento do cache no CLI.

**1)** Verifica se o produto já está em cache (simule rodando isto primeiro: em um sistema real haveria um `cache miss` aqui).
```
GET cache:produto:101
```

**2)** Como não existe (cache miss), a aplicação "consultaria o SQL Server" e agora grava o resultado no cache, com expiração de 5 minutos (300s).
```
SET cache:produto:101 "{\"nome\":\"Notebook Gamer\",\"preco\":5999.90}" EX 300
```

**3)** Nova consulta ao mesmo produto — agora é um cache hit, resposta instantânea, sem tocar no banco relacional.
```
GET cache:produto:101
```

**4)** Verifica quanto tempo falta para o cache expirar.
```
TTL cache:produto:101
```

**5)** Invalidação manual do cache (ex.: o preço do produto mudou no banco relacional e o cache ficou desatualizado).
```
DEL cache:produto:101
```

---

## Aplicação 2 — Sessão de Usuário

**Contexto:** ao logar, o usuário recebe um token de sessão com dados básicos e tempo de vida limitado.

**1)** Cria a sessão do usuário 55, associada a um token, com todos os dados relevantes.
```
HSET sessao:af31c9 usuario_id 55 nome "Ana Souza"
```

**2)** Define o tempo de vida da sessão (30 minutos = 1800 segundos).
```
EXPIRE sessao:af31c9 1800
```

**3)** A cada requisição do usuário, o sistema valida se a sessão ainda existe.
```
EXISTS sessao:af31c9
```

**4)** Sessão válida: renova o tempo de vida (sliding expiration) e lê os dados do usuário logado.
```
EXPIRE sessao:af31c9 1800
HGETALL sessao:af31c9
```

**5)** Logout manual: encerra a sessão antes mesmo dela expirar sozinha.
```
DEL sessao:af31c9
```

---

## Aplicação 3 — Fila de Pedidos + Pub/Sub

**Contexto:** ao finalizar uma compra, o pedido entra em uma fila (garantida) e, opcionalmente, uma notificação é publicada em tempo real (não garantida).

**1)** Checkout do usuário 55 gera um pedido, que é inserido na fila de processamento.
```
LPUSH fila:pedidos "{\"usuario_id\":55,\"pedido_id\":301}"
```

**2)** O time de logística processa o próximo pedido da fila (bloqueia até 5s esperando, se estiver vazia).
```
BRPOP fila:pedidos 5
```

**3)** Em paralelo, o sistema publica uma notificação em tempo real sobre o novo pedido (rode em um segundo terminal `SUBSCRIBE canal:pedidos` antes deste comando, para ver a mensagem chegando).
```
PUBLISH canal:pedidos "Novo pedido #301 recebido!"
```

**4)** Assinar o canal de notificações (rodar em um terminal/CLI separado, ele fica "escutando").
```
SUBSCRIBE canal:pedidos
```

---

## Aplicação 4 — Rate Limiting

**Contexto:** protege uma "API" de consulta contra abuso, limitando a 5 requisições a cada 10 segundos por IP.

**1)** Primeira requisição do IP: cria o contador da janela e já define quando ela expira.
```
INCR rate_limit:200.150.10.5
EXPIRE rate_limit:200.150.10.5 10
```

**2)** Mais 4 requisições rápidas do mesmo IP (ainda dentro do limite de 5).
```
INCR rate_limit:200.150.10.5
INCR rate_limit:200.150.10.5
INCR rate_limit:200.150.10.5
INCR rate_limit:200.150.10.5
```

**3)** 6ª requisição: o valor já passa de 5 → a aplicação deve bloquear (checagem feita no código, não pelo Redis).
```
INCR rate_limit:200.150.10.5
```

**4)** Verifica quanto tempo falta para o limite resetar.
```
TTL rate_limit:200.150.10.5
```

**5)** Após a janela expirar (aguarde os segundos indicados pelo TTL), a chave não existe mais e uma nova janela começa do zero.
```
EXISTS rate_limit:200.150.10.5
```

---

## Aplicação 5 — Leaderboard (Ranking em Tempo Real)

**Contexto:** ranking de pontuação de jogadores em um jogo/gamificação, sempre ordenado automaticamente.

**1)** Cadastra a pontuação inicial de 3 jogadores.
```
ZADD ranking:jogo1 1500 "ana" 2100 "leo" 1800 "carla"
```

**2)** Consulta o pódio (Top 3) em ordem decrescente, com pontuação.
```
ZREVRANGE ranking:jogo1 0 2 WITHSCORES
```

**3)** A jogadora "ana" pontua mais 300 pontos em uma nova partida (soma atômica).
```
ZINCRBY ranking:jogo1 300 "ana"
```

**4)** Verifica a nova posição de "ana" no ranking (0 = 1º lugar).
```
ZREVRANK ranking:jogo1 "ana"
```

**5)** Consulta apenas a pontuação atual de um jogador específico.
```
ZSCORE ranking:jogo1 "leo"
```

**6)** Jogador "carla" é removido do ranking (ex.: encerrou a conta no jogo).
```
ZREM ranking:jogo1 "carla"
```
