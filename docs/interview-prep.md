# Preparacao para Entrevista

Responda cada pergunta em 1 a 3 minutos, usando exemplos concretos do projeto. Depois podemos revisar clareza, profundidade tecnica e impacto.

## Rodada 1

1. Como voce estruturou o AI Operations Agent para evitar que um unico agente concentrasse todas as responsabilidades?

2. Por que o sistema usa um estado compartilhado entre agentes? Quais informacoes entram nesse estado e como voce evita que um agente sobrescreva dados de outro fluxo?

3. Como o Data Agent e o Knowledge Agent trabalham juntos? Explique a diferenca entre dados transacionais do cliente e documentos de politica ou procedimento.

4. Como o Root Cause Agent decide o nivel de risco sem inventar informacoes? Cite as evidencias que ele considera e o comportamento quando elas sao insuficientes.

5. Quais regras fazem o Decision Agent escalar um caso para a equipe tecnica? Como voce registraria essas regras para auditoria?

6. Como voce protegeria a resposta final contra vazamento de dados internos, prompt injection e afirmacoes sem evidencia?

7. Por que voce comecou com um retriever lexical deterministico em vez de embeddings? Em que momento faria a troca por um vector store?

8. Como voce testaria esse sistema em producao? Considere testes unitarios, avaliacao de respostas, observabilidade e falhas da API da OpenAI.

## Respostas modelo

### 1. Como voce estruturou o sistema?

"Eu separei o sistema em agentes especializados, cada um com uma responsabilidade clara. Tenho agentes para orquestracao, analise do cliente, consulta de dados, recuperacao de conhecimento, causa raiz, decisao, resposta e avaliacao. Eles compartilham um estado controlado, mas cada agente altera apenas a parte relacionada a sua responsabilidade. Isso reduz acoplamento e facilita testar e substituir componentes individualmente."

### 2. Por que usar um estado compartilhado?

"O estado compartilhado funciona como o contrato do fluxo. Ele transporta a solicitacao, o cliente, o historico, a classificacao, os documentos recuperados, a causa raiz, a decisao, a resposta e a avaliacao. Eu uso chaves explicitas e registro metadados de execucao para rastreabilidade. A ideia e evitar que os agentes dependam diretamente uns dos outros ou executem consultas fora de suas responsabilidades."

### 3. Como Data Agent e Knowledge Agent trabalham juntos?

"O Data Agent consulta dados transacionais, como cadastro, tickets, interacoes e metricas do cliente. O Knowledge Agent consulta documentos operacionais, como politicas de garantia e procedimentos de escalonamento. O primeiro responde o que aconteceu com aquele cliente; o segundo responde quais regras e procedimentos podem ser aplicados. O Root Cause Agent combina os dois tipos de evidencia."

### 4. Como o Root Cause Agent evita inventar informacoes?

"Ele trabalha somente com campos presentes no estado: classificacao, tickets anteriores, metricas e documentos recuperados. Recorrencia, tickets abertos e prioridade alta podem elevar o risco, mas isso e registrado como fator contribuinte, nao como certeza absoluta. Quando nao existem evidencias suficientes, ele marca a causa como nao confirmada e recomenda coletar mais informacoes."

### 5. Como o Decision Agent decide escalar?

"Eu defini regras deterministicas. Casos de risco alto sao escalados. Tambem escalo quando existe prioridade alta ou critica combinada com recorrencia ou tickets abertos. Casos medios continuam em investigacao e casos de baixo risco recebem orientacao inicial. A decisao, a justificativa e as evidencias usadas ficam registradas para auditoria."

### 6. Como proteger a resposta final?

"Eu separo informacoes internas da mensagem do cliente. O Response Agent usa somente o proximo passo aprovado e nao expoe recomendacoes internas. Tambem aplico validacao contra prompt injection, mantenho a chave da OpenAI em variavel de ambiente e uso o Evaluation Agent para detectar marcadores internos, respostas vazias ou sinais de risco de alucinacao antes da entrega."

### 7. Por que comecar com busca lexical?

"Comecei com um retriever lexical porque ele e deterministico, barato e facil de testar com a base pequena do prototipo. A interface ja retorna fonte, score e termos encontrados, entao posso trocar a implementacao por embeddings e vector store quando o volume, a variedade dos documentos e a necessidade de similaridade semantica justificarem essa complexidade."

### 8. Como testar em producao?

"Eu combinaria testes unitarios dos agentes, testes de integracao do fluxo, casos de avaliacao para respostas e testes de falha da API. Tambem acompanharia latencia, taxa de escalonamento, falhas por agente, qualidade das respostas e risco de alucinacao. Os metadados de execucao, as fontes recuperadas e as decisoes ajudariam a investigar regressao sem registrar segredos ou dados desnecessarios."
