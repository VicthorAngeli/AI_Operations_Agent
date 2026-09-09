# Security Policy

## Reporting a vulnerability

Do not open a public issue with credentials, exploit details, or customer data. Report suspected vulnerabilities privately to the repository owner through GitHub or the contact method listed on the owner profile.

## Deployment requirements

- Set `API_AUTH_TOKEN` in production.
- Keep `OPENAI_API_KEY` outside the repository and inject it through a secret manager or environment variable.
- Protect `/analyze`, `/metrics`, and `/executions/{execution_id}` behind authentication.
- Use HTTPS and a shared rate-limit store or gateway for multiple replicas.