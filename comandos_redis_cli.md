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

# Boas Práticas em Produção — Comandos e Exemplos

**Como usar:** copie e cole os blocos de comando, em ordem, no `redis-cli` ou no
**Workbench do RedisInsight**. Cada seção corresponde a um dos 6 cards do slide
"Boas Práticas em Produção".

---

## 1. Nomeie chaves com padrão

**Contexto:** usar namespaces com `:` organiza as chaves por entidade e facilita buscas, backups seletivos e leitura do código.

**1)** Nomenclatura recomendada — hierarquia clara `entidade:id:atributo`.
```
SET usuario:102:perfil "dados do perfil"
SET usuario:102:carrinho "dados do carrinho"
```

**2)** Com o padrão, fica fácil localizar tudo relacionado a um usuário específico (uso pontual — não rodar com bases grandes em produção, ver item 3).
```
KEYS usuario:102:*
```

**❌ Evite:** nomes sem padrão, como `dadosUser102`, `carrinho_102_v2`, `tempUser` — impossível de filtrar, agrupar ou dar manutenção depois.

---

## 2. Sempre defina TTL quando fizer sentido

**Contexto:** dados temporários (sessões, cache, promoções, códigos de verificação) devem expirar sozinhos, evitando crescimento infinito de memória.

**1)** Cria a chave já com expiração embutida (30 minutos = 1800 segundos).
```
SET sessao:abc123 "token-do-usuario" EX 1800
```

**2)** Verifica quanto tempo de vida resta.
```
TTL sessao:abc123
```

**3)** Define (ou redefine) o TTL de uma chave que já existe.
```
EXPIRE sessao:abc123 1800
```

**4)** Remove o TTL, tornando a chave permanente (use com cautela — é o oposto do que normalmente se quer).
```
PERSIST sessao:abc123
```

**❌ Evite:** criar chaves de sessão/cache/código-de-verificação com `SET` simples, sem `EX`/`EXPIRE` — elas nunca expiram e ficam ocupando memória para sempre.

---

## 3. Nunca use KEYS * em produção

**Contexto:** `KEYS` varre o banco inteiro de uma vez e bloqueia o servidor (o Redis é single-thread) — em bases grandes isso pode travar todas as outras requisições por segundos. Use `SCAN`, que percorre aos poucos, sem bloquear.

**1) ❌ Não faça isso em produção** (funciona, mas trava o servidor em bases grandes):
```
KEYS produto:*
```

**2) ✅ Alternativa segura** — itera em pequenos lotes (`COUNT` sugere o tamanho do lote), sem bloquear o servidor.
```
SCAN 0 MATCH produto:* COUNT 10
```

**3)** O `SCAN` retorna um **cursor** (um número) junto com o lote de chaves. Para continuar, rode o comando de novo passando esse cursor no lugar do `0`, até ele voltar a ser `0` (fim da varredura).
```
SCAN 26 MATCH produto:* COUNT 10
```

**Equivalente para outras estruturas:** assim como `KEYS` tem o `SCAN`, os comandos abaixo também têm suas versões "com cursor" — usadas no item 6.
- `HSCAN` (para campos de um Hash)
- `SSCAN` (para membros de um Set)
- `ZSCAN` (para membros de um Sorted Set)

---

## 4. Monitore o uso de memória

**Contexto:** o Redis guarda tudo em RAM — sem monitoramento, o servidor pode ficar sem memória disponível e começar a recusar escritas (ou pior, derrubar o processo).

**1)** Visão geral do consumo de memória do servidor.
```
INFO memory
```

**2)** Quanto de memória uma chave específica está ocupando (em bytes) — útil para achar "chaves gigantes" que merecem atenção.
```
MEMORY USAGE produto:1
```

**3)** Consulta a política atual de remoção de chaves quando a memória máxima é atingida.
```
CONFIG GET maxmemory-policy
```

**4)** Define a política para descartar automaticamente as chaves menos usadas recentemente (LRU) quando a memória máxima (`maxmemory`) é atingida — evita que o Redis simplesmente pare de aceitar escritas.
```
CONFIG SET maxmemory-policy allkeys-lru
```

**Políticas mais comuns de `maxmemory-policy`:**
| Política | Comportamento |
|---|---|
| `noeviction` (padrão) | Recusa novas escritas quando a memória enche — **não perde dados**, mas quebra a aplicação. |
| `allkeys-lru` | Remove as chaves menos acessadas recentemente, entre **todas** as chaves. |
| `volatile-lru` | Remove as menos acessadas, mas **só entre as chaves que têm TTL definido**. |
| `volatile-ttl` | Remove primeiro as chaves com TTL mais próximo de expirar. |

---

## 5. Habilite autenticação e TLS

**Contexto:** por padrão, um Redis local não exige senha — inaceitável se o servidor for exposto em rede. Em produção (como no Redis Cloud que já usamos), use senha (ou ACL) e conexão criptografada (TLS).

**1)** Verifica qual usuário está autenticado na conexão atual.
```
ACL WHOAMI
```

**2)** Lista os usuários/regras de acesso configurados no servidor.
```
ACL LIST
```

**3)** Define uma senha simples para o usuário padrão (forma mais básica de autenticação — o Redis Cloud já faz isso por você).
```
CONFIG SET requirepass "minhaSenhaForte123"
```

**4)** A partir daí, toda nova conexão precisa se autenticar antes de rodar qualquer comando.
```
AUTH minhaSenhaForte123
```

**5) (Mais avançado)** Cria um usuário com permissão **apenas de leitura**, restrito a um padrão de chaves — útil para dar acesso a um serviço de relatórios, por exemplo, sem risco de ele escrever ou apagar dados.
```
ACL SETUSER relatorios on >senhaRelatorios ~produto:* +get +mget
```

**❌ Evite:** deixar `requirepass` vazio (ou usar a senha default) em qualquer ambiente acessível pela internet — é a causa mais comum de "sequestro" de instâncias Redis mal configuradas.

---

## 6. Cuidado com comandos O(N)

**Contexto:** comandos como `SMEMBERS`, `LRANGE` (sem limite), `HGETALL` e `KEYS` custam tempo proporcional ao **tamanho da coleção** — em coleções grandes, isso pode travar o event loop do Redis (lembre-se: é single-thread).

**1)** Cria um set com vários itens, simulando uma coleção que cresceu com o tempo.
```
SADD tags:grande tag1 tag2 tag3 tag4 tag5 tag6 tag7 tag8 tag9 tag10
```

**2) ❌ Arriscado em coleções muito grandes** — traz **todos** os itens de uma vez.
```
SMEMBERS tags:grande
```

**3) ✅ Alternativa paginada** — traz um lote por vez, sem travar o servidor, igual ao `SCAN` do item 3.
```
SSCAN tags:grande 0 COUNT 5
```

**4)** O mesmo cuidado vale para Listas: evite ler tudo de uma vez em listas grandes...
```
LRANGE fila:pedidos 0 -1
```
**5)** ...prefira ler em páginas menores, especificando um intervalo (aqui, os 10 primeiros itens).
```
LRANGE fila:pedidos 0 9
```

---

## Resumo rápido (cheat sheet desta seção)

| Boa prática | Comando-chave |
|---|---|
| Nomear chaves com padrão | `entidade:id:atributo` |
| Definir TTL | `EXPIRE`, `SET ... EX`, `TTL`, `PERSIST` |
| Evitar `KEYS *` | `SCAN cursor MATCH padrão COUNT n` |
| Monitorar memória | `INFO memory`, `MEMORY USAGE`, `CONFIG SET maxmemory-policy` |
| Autenticação e TLS | `ACL WHOAMI`, `ACL LIST`, `ACL SETUSER`, `AUTH` |
| Evitar comandos O(N) | `SSCAN`, `HSCAN`, `ZSCAN`, `LRANGE` com intervalo limitado |
