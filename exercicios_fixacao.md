# Exercícios de Fixação — Bancos de Dados Chave-Valor (Redis)

**Disciplina:** Banco de Dados Não Relacional
**Curso:** Análise e Desenvolvimento de Sistemas — 3º semestre
**Tema:** Modelo Chave-Valor, Teorema CAP, CRUD e aplicações com Redis

> Use o `redis-cli` ou um script Python (com `redis-py`) para resolver os exercícios práticos. Sempre que possível, teste seus comandos antes de escrever a resposta final.

---

## Parte 1 — Conceitos e Teorema CAP (teórica)

**1.1)** Explique, com suas próprias palavras, a diferença entre um banco de dados chave-valor e um banco de dados relacional. Cite pelo menos duas situações em que o modelo chave-valor é vantajoso e duas em que ele é desvantajoso.

**1.2)** O Teorema CAP afirma que um sistema distribuído só pode garantir 2 das 3 propriedades (Consistência, Disponibilidade, Tolerância a Partição) simultaneamente. Explique por que, na prática, a Tolerância a Partição (P) não costuma ser uma escolha, e qual é o verdadeiro trade-off que resta ao arquiteto de software.

**1.3)** Classifique os sistemas abaixo como **CP** ou **AP** e justifique cada resposta em 1-2 frases:
   a) Um sistema bancário que processa transferências entre contas.
   b) Um contador de "curtidas" em uma rede social.
   c) Um sistema de estoque de e-commerce, no momento do checkout.
   d) Um feed de notícias que agrega postagens de amigos.

**1.4)** Um colega de equipe afirma: "Vamos usar Redis Cluster porque ele nos dá Consistência E Disponibilidade totais, mesmo durante uma falha de rede." Aponte o erro conceitual dessa afirmação.

**1.5)** Explique o conceito de **consistência eventual** e dê um exemplo prático (fora dos vistos em aula) de uma aplicação onde ela seria aceitável, e outro onde ela seria inaceitável.

---

## Parte 2 — CRUD com redis-cli (prática)

Utilize o `redis-cli` (ou o painel de comandos do Redis Cloud) para resolver os exercícios abaixo. Anote os comandos utilizados.

**2.1)** Crie uma chave `curso:nome` com o valor `"Banco de Dados Não Relacional"` e uma chave `curso:semestre` com o valor `3`. Em seguida, leia as duas chaves com um único comando.

**2.2)** Crie a chave `token:acesso` com o valor `"abc123"` e defina que ela deve expirar em 20 segundos. Verifique o tempo restante de vida com o comando adequado. Espere a expiração e confirme que a chave não existe mais.

**2.3)** Crie um hash `produto:10` com os campos `nome`, `preco` e `estoque`. Depois:
   a) Leia apenas o campo `preco`.
   b) Diminua o campo `estoque` em 3 unidades (pesquise o comando adequado para decrementar).
   c) Leia o hash inteiro.

**2.4)** Crie uma lista chamada `fila:atendimento` e insira, nesta ordem, os nomes `"Cliente A"`, `"Cliente B"` e `"Cliente C"`, de forma que `"Cliente A"` seja o primeiro a ser atendido (fila FIFO). Depois, "atenda" (remova) o primeiro cliente da fila e mostre quem restou.

**2.5)** Crie um set chamado `interesses:usuario1` com os valores `"redis"`, `"python"` e `"banco-de-dados"`. Tente adicionar `"redis"` novamente e explique o que acontece. Depois, verifique se `"mongodb"` está no conjunto.

**2.6)** Crie um sorted set chamado `ranking:vendas` com 4 vendedores e suas respectivas quantidades de vendas. Consulte os 2 melhores vendedores em ordem decrescente, com suas pontuações.

---

## Parte 3 — Python + Redis (prática)

Crie um único script Python (`exercicio_parte3.py`) que resolva os itens abaixo, na ordem. Use `redis-py`.

**3.1)** Conecte-se ao Redis (local ou Redis Cloud) e imprima o resultado de `PING`.

**3.2)** Crie um hash `aluno:<seu_numero_de_matricula>` com os campos `nome`, `curso` e `semestre`. Leia e imprima o hash completo.

**3.3)** Implemente uma função `contar_acesso(pagina: str) -> int` que incremente um contador de acessos para a página informada (chave `acessos:<pagina>`) e retorne o novo valor total. Teste chamando a função 5 vezes para a página `"home"`.

**3.4)** Implemente uma função `adicionar_favorito(usuario_id: int, produto_id: int)` que adicione o `produto_id` a um **set** de favoritos do usuário (chave `favoritos:<usuario_id>`), e uma função `listar_favoritos(usuario_id: int)` que retorne todos os favoritos daquele usuário.

**3.5)** Implemente uma função `registrar_pontuacao(jogador: str, pontos: int)` que utilize um **sorted set** chamado `ranking:desafio` para registrar a pontuação de um jogador (some a pontos existentes, se houver). Ao final do script, imprima o Top 3 jogadores.

**3.6) (Desafio)** Implemente uma função `esta_dentro_do_limite(usuario_id: int, limite: int, janela_segundos: int) -> bool` que funcione como um rate limiter simples (semelhante ao visto em aula), usando `INCR` e `EXPIRE`. Escreva um pequeno teste que simule 10 chamadas seguidas com `limite=4` e mostre quais foram aceitas e quais foram bloqueadas.

---

## Parte 4 — Análise crítica (teórica/discursiva)

**4.1)** Sua equipe está desenvolvendo um sistema de matrícula acadêmica (como o SIGAA/Q-Acadêmico). Você defenderia o uso do Redis como **banco de dados principal** desse sistema? Justifique tecnicamente considerando o Teorema CAP e os tipos de consulta necessários.

**4.2)** Ainda sobre o sistema de matrícula: em quais partes específicas desse sistema o Redis PODERIA ser adotado como **camada complementar** ao banco relacional? Cite pelo menos 3 casos de uso concretos.

**4.3)** Compare, em uma tabela, o Redis e o MongoDB (já estudado anteriormente na disciplina) em relação a: modelo de dados, linguagem de consulta, casos de uso típicos e posicionamento no Teorema CAP.

**4.4)** Pesquise (fora da aula) sobre o comando `EXPIRE` e o conceito de **eviction policies** (ex.: `noeviction`, `allkeys-lru`, `volatile-ttl`). Explique o que aconteceria com os dados do seu sistema caso a memória do servidor Redis se esgotasse, sob a política `noeviction` versus `allkeys-lru`.

---

## Critérios de Entrega

- Entregar um único arquivo `.pdf` ou `.docx` com as respostas da Parte 1 e Parte 4.
- Entregar os scripts `.py` das Partes 2 e 3 (pode ser um arquivo por parte, ou um único arquivo comentado).
- Print ou log de execução dos comandos/scripts deve ser incluído como evidência.
- Prazo e formato de entrega: conforme combinado em sala / AVA da instituição.
