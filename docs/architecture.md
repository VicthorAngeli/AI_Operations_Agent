# Documentação de Arquitetura

## Visão geral

Este projeto implementa um sistema multiagente para automação operacional de atendimento ao cliente. A estrutura combina:

- orquestração em LangGraph;
- agentes especializados;
- RAG para base de conhecimento;
- SQLite para dados simulados;
- FastAPI para API REST;
- Streamlit para interface visual.

## Componentes principais

### 1. Orquestrador
O agente principal coordena o fluxo de execução e utiliza um estado compartilhado para transportar informações entre nós.

### 2. Agentes especializados
Os agentes têm responsabilidades bem delimitadas para reduzir ambiguidade e melhorar rastreabilidade.

### 3. Base de dados
Os dados de clientes, produtos, tickets e interações ficam em SQLite, com repository/service abstração para evitar acesso SQL direto nos agentes.

### 4. RAG
Os documentos fictícios de políticas e procedimentos ficam em `data/knowledge_base`. O `KnowledgeRetriever` faz uma recuperação lexical determinística e retorna score, termos encontrados, conteúdo e fonte. Essa interface mantém o agente desacoplado do mecanismo de indexação e permite evoluir para embeddings e vector store sem alterar o estado compartilhado.

### 5. API e interface
A solução expõe endpoints REST e uma interface em Streamlit, permitindo uso por cliente interno ou demonstração.

## Fluxo de dados

1. O usuário envia a solicitação e o `customer_id`.
2. O Orchestrator cria uma execução e prepara o estado.
3. O Customer Analysis Agent extrai classificação e sentimento.
4. O Data Agent consulta histórico e produto.
5. O Knowledge Agent busca políticas relevantes.
6. O Root Cause Agent identifica riscos e causa provável.
7. O Decision Agent define a ação apropriada.
8. O Response Agent gera a mensagem final.
9. O Evaluation Agent revisa qualidade e risco de alucinação.
10. O resultado é persistido e retornado ao usuário.

### 5. Análise de causa raiz

O `RootCauseAgent` não inventa evidências: ele combina classificação, tickets anteriores, métricas do cliente e documentos recuperados. Recorrência, tickets abertos e prioridade alta elevam o risco; quando não há evidência suficiente, o agente marca a causa como não confirmada e recomenda coletar mais informações.

### 6. Decisão operacional

O `DecisionAgent` converte o risco e a classificação em três resultados controlados: `escalate_technical`, `continue_investigation` ou `provide_initial_guidance`. Casos de alto risco, ou de alta prioridade com recorrência ou tickets abertos, são escalonados. A decisão e os dados considerados ficam registrados no estado para auditoria e para os agentes de resposta e avaliação.

### 7. Resposta e avaliação

O `ResponseAgent` transforma a decisão em uma mensagem externa sem expor recomendações internas. Em seguida, o `EvaluationAgent` verifica a presença de conteúdo, alinhamento com a decisão, clareza, completude e marcadores de informação interna. O resultado da avaliação fica no estado antes da entrega ao consumidor.

### 8. Execução integrada

O executor em `app/graph/workflow.py` inicializa o banco, valida a entrada, aplica o guardrail de prompt injection e executa os oito agentes em ordem. O endpoint `POST /analyze` converte a solicitação HTTP em estado, executa o fluxo e retorna classificação, decisão, resposta final e avaliação.

### 9. Interface operacional

O Streamlit funciona como cliente da API, sem duplicar regras de negócio. Ele envia a solicitação para `POST /analyze`, apresenta a resposta e a avaliação e consulta `GET /executions/{execution_id}` para exibir a auditoria da execução.

### 10. Empacotamento

O `Dockerfile` cria uma imagem comum para a API e o frontend. O `docker-compose.yml` executa os dois serviços, aguarda o healthcheck da API antes de iniciar o Streamlit e usa um volume nomeado para preservar o SQLite em `/app/runtime`. A chave da OpenAI é recebida por variável de ambiente e não é copiada para a imagem.

### 11. Integração contínua

O workflow `.github/workflows/ci.yml` executa a compilação dos módulos Python, a suíte de testes e o build da imagem Docker. O job de container depende do job de testes, evitando validar uma imagem que já contenha uma regressão conhecida.

### 12. Endurecimento da API

O serviço aplica CORS por lista de origens configurável, headers básicos contra conteúdo MIME indevido, framing e referrer leakage, além de um endpoint `/ready` que verifica o acesso ao SQLite. O endpoint `/health` continua sendo um sinal simples de processo ativo; `/ready` indica que a dependência de dados está disponível.

### 13. Métricas

O endpoint `/metrics` expõe métricas em formato compatível com Prometheus: total de requisições por método e status, duração HTTP agregada e resultados do workflow por sucesso ou falha. O registro é mantido em memória para o protótipo; em produção, deve ser substituído ou integrado a um backend de métricas externo.

### 14. Proteção contra abuso

O endpoint `/analyze` aplica um limite fixo por endereço IP e retorna `429` com `Retry-After` quando a janela é excedida. Os valores são configurados por `RATE_LIMIT_REQUESTS` e `RATE_LIMIT_WINDOW_SECONDS`. Como o contador é local ao processo, ambientes com múltiplas réplicas devem aplicar o limite no gateway ou em um armazenamento compartilhado.

### 15. Autenticação de API

Em produção, `/analyze`, `/metrics` e `/executions/{execution_id}` exigem o header `X-API-Key`, comparado em tempo constante com `API_AUTH_TOKEN`. O token é recebido por ambiente e nunca é incluído no código, na imagem ou no repositório.

## Segurança

- Chave da OpenAI via ambiente
- validação de entradas
- logs controlados
- rejeição de prompt injection
- limite de contexto e regras de negócio rigidamente controladas

## Observabilidade

Os registros de execução devem armazenar:

- execution_id
- agente executado
- timestamp
- duração
- ferramenta utilizada
- erro e contexto

Na fase 10, cada agente grava `execution_id`, timestamps, duração e um resumo técnico não sensível na tabela `agent_executions`. O endpoint `GET /executions/{execution_id}` permite consultar a ordem e o tempo dos agentes sem retornar a mensagem original do cliente.

## Extensibilidade

A arquitetura permite evoluir para:

- PostgreSQL em vez de SQLite;
- vector store externo;
- integrações com CRM real;
- workflows com outros canais e eventos.
