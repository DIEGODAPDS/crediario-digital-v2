# Crediário Digital Web pronto para Render

## Como subir no GitHub
1. Apague do repositório antigo os arquivos que não precisa, se quiser.
2. Envie todos os arquivos desta pasta para o GitHub.
3. Confirme que existe a pasta `web` no repositório.

## Render
Build Command:
```text
pip install -r requirements-web.txt
```
Start Command:
```text
uvicorn web.app:app --host 0.0.0.0 --port $PORT
```

## Variáveis no Render
```text
CREDIARIO_DB_BACKEND=postgresql
CREDIARIO_DATABASE_URL=postgresql://usuario:senha@host:5432/banco?sslmode=require
SECRET_KEY=uma-chave-grande-e-secreta
```

Primeiro acesso: admin / admin
