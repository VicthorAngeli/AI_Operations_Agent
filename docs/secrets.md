# Secrets e configuração de produção

Não existe uma chave real no repositório. Preencha `.env.production.example` apenas no ambiente de execução ou configure os valores em um secret manager.

Variáveis obrigatórias ou sensíveis:

- `OPENAI_API_KEY`: chave da API da OpenAI.
- `API_ALLOWED_ORIGINS`: origens autorizadas para o frontend.
- `DATABASE_URL`: caminho do SQLite persistente.

Variáveis operacionais:

- `OPENAI_MODEL`
- `OPENAI_TEMPERATURE`
- `RATE_LIMIT_REQUESTS`
- `RATE_LIMIT_WINDOW_SECONDS`

Para Docker Compose, exporte `OPENAI_API_KEY` no shell antes de executar `docker compose up --build`. Não coloque o valor diretamente no `docker-compose.yml`, no código ou em commits.