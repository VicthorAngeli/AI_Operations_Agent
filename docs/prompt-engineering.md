# Prompt Engineering

## Objetivo
A engenharia de prompt desta solução evita que os agentes trabalhem com instruções genéricas demais. Cada agente tem uma responsabilidade específica e um prompt especializado.

## Princípios

### 1. Papel claro
Cada agente recebe um papel específico, com limites e objetivos bem definidos.

### 2. Contexto mínimo relevante
A entrada do modelo contém somente o contexto que importa para a decisão atual, reduzindo ruído.

### 3. Saída estruturada
A utilização de Pydantic e schemas reduz ambiguidades e produz resultados previsíveis.

### 4. Guardrails
Regras e políticas são incorporadas para impedir que o modelo ignore instruções críticas.

### 5. RAG para evitar dependência excessiva de memória interna
A base de conhecimento fornece contexto real, diminuindo a necessidade do modelo inventar políticas.

### 6. Regras determinísticas + IA
Os agentes de decisão usam lógica programática para eventos críticos e deixam a IA justificar a decisão.

## Exemplos de problemas evitados

- prompt injection tentando mudar regras internas;
- respostas vagas sem estrutura;
- alucinação sobre políticas ou garantia;
- decisões inconsistentes por falta de contexto.

## Como isso se aplica aos agentes

- Customer Analysis: foco em classificação e sentimento.
- Data Agent: foco em consulta controlada e uso de ferramentas.
- Knowledge Agent: foco em recuperação semântica de políticas.
- Decision Agent: foco em ação correta com base em regras e evidências.
- Response Agent: foco em comunicação profissional e segura.
- Evaluation Agent: foco em revisar qualidade, aderência e risco.

## Conclusão
A combinação de prompts especializados, structured output e políticas de segurança reduz erros, melhora confiabilidade e torna a arquitetura mais adequada para uso profissional.
