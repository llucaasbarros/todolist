# To-Do List

Gerenciador de tarefas, teste técnico. Django REST Framework + React, tudo em Docker.

## Stack

Backend: Django 5.2, DRF, JWT (simplejwt), Postgres, pytest, drf-spectacular (Swagger).
Frontend: React 18, Vite, react-router-dom, axios, CSS puro.
Testes: pytest (backend, com cobertura) e Selenium (frontend).
CI: GitHub Actions, ruff no backend, eslint no frontend.

## Como rodar

Precisa de Docker e Docker Compose.

Clona, copia as variáveis de ambiente e builda + sobe os containers (db, backend, frontend):

```
git clone https://github.com/llucaasbarros/todolist.git
cd todolist
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
docker compose up -d
```

Migrations rodam sozinhas no start do backend.

Pra buildar cada um separado, sem subir os dois juntos:

```
docker compose build backend
docker compose build frontend
```

frontend: http://localhost:5183
admin: http://localhost:8000/admin
api: http://localhost:8000/api
docs (swagger): http://localhost:8000/api/docs/

Superusuário pro admin:

```
docker compose exec backend python src/manage.py createsuperuser
```

## Variáveis de ambiente

`.env` da raiz: usuário/senha do Postgres. `backend/.env`: mesmas credenciais + config do Django. `frontend/.env`: URL da API.

## Testes

Testes do backend, com e sem relatório de cobertura:
```
docker compose exec backend pytest --cov=apps --cov-report=term-missing
docker compose exec backend pytest
```

Lint e build do frontend:
```
cd frontend
npm run lint
npm run build
```

Testes end-to-end com Selenium, precisa da stack rodando:
```
cd frontend/e2e
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pytest -v
```

## Estrutura

Backend, `backend/src/apps/`:

- `core`: model abstrata (TimeStampedModel), sem tabela própria.
- `accounts`: usuário customizado, registro e login.
- `categories`: CRUD de categoria, isolado por dono.
- `tasks`: CRUD de tarefa, compartilhamento, filtro, paginação.
- `holidays`: feriados nacionais via BrasilAPI.

Frontend, `frontend/src/`:

- `api`: chamadas HTTP por recurso.
- `features/<nome>/views`: telas.
- `features/<nome>/components`: pedaços de cada feature.
- `components`: genéricos (layout, paginação, toast).
- `contexts`/`hooks`: auth e outros estados globais.

## Decisões de design

- Usuário customizado desde o início, evita migração dolorosa depois.
- Isolamento por usuário no get_queryset, não só no frontend.
- Compartilhamento é só leitura, garantido por permission class.
- Feriados via BrasilAPI, aparecem quando o vencimento cai num feriado.
- Sem lib de UI, CSS puro.
- Frontend em produção atrás de nginx, build multi-stage.
- Selenium roda num container próprio, sem instalar Chrome local.

## Deploy

Guia de deploy em AWS ECS (Fargate) em [DEPLOY.md](DEPLOY.md). Não roda sozinho — é um workflow manual, disparado só depois de provisionar a infra.
