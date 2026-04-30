# Crediário Digital Web

Primeira versão web do Crediário Digital, criada para rodar online com FastAPI e PostgreSQL.

## O que já está disponível

- Login com o usuário existente do sistema.
- Painel com resumo de clientes, parcelas abertas, atrasadas e vencimentos do dia.
- Cadastro, edição, remoção lógica e histórico de clientes.
- Lançamento de venda com geração automática de parcelas.
- Consulta de parcelas por status, rota, período e pesquisa textual.
- Baixa de parcelas, incluindo pagamento parcial com geração automática do saldo restante.
- Reversão de baixa.

## Rodar localmente

```powershell
py -3 -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-web.txt
.\.venv\Scripts\python.exe -m uvicorn web.app:app --reload
```

Acesse:

```text
http://127.0.0.1:8000
```

Primeiro acesso:

```text
admin / admin
```

## Banco para acesso online

Para hospedar online, use PostgreSQL. SQLite deve ficar apenas para teste local.

Variáveis de ambiente esperadas:

```text
CREDIARIO_DB_BACKEND=postgresql
CREDIARIO_DATABASE_URL=postgresql://usuario:senha@host:5432/banco?sslmode=require
SECRET_KEY=uma-chave-grande-e-secreta
```

Se a URL do banco não tiver `sslmode=require`, configure também:

```text
CREDIARIO_DB_SSLMODE=require
```

## Hospedagem gratuita sugerida

Caminho simples:

1. Crie um banco PostgreSQL gratuito no Neon.
2. Copie a connection string do banco.
3. Suba este projeto para um repositório GitHub.
4. No Render, crie um Web Service gratuito conectado ao repositório.
5. Configure:

```text
Build Command: pip install -r requirements-web.txt
Start Command: uvicorn web.app:app --host 0.0.0.0 --port $PORT
```

6. Adicione as variáveis `CREDIARIO_DB_BACKEND`, `CREDIARIO_DATABASE_URL` e `SECRET_KEY`.

O arquivo `render.yaml` já deixa esses comandos prontos para o Render.

## Avisos importantes

- Plano gratuito pode dormir por inatividade e ter limites de uso.
- Para produção real, configure backups do PostgreSQL por fora do aplicativo.
- Troque a senha `admin` no primeiro acesso.
- Não envie o arquivo `.env` nem bancos `.sqlite3` para o GitHub.
