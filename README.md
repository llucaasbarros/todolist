# To-Do List

Gerenciador de tarefas, teste técnico. Django REST Framework + React, tudo em Docker.

## Stack

Backend: Django 5.2, DRF, JWT (simplejwt), Postgres, pytest, drf-spectacular (Swagger).
Frontend: React 18, Vite, react-router-dom, axios, CSS puro.
Testes: pytest (backend, com cobertura) e Selenium (frontend).
CI: GitHub Actions, ruff no backend, eslint no frontend.

## Como rodar

Precisa de Docker e Docker Compose.

```
git clone https://github.com/llucaasbarros/todolist.git
cd todolist
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
docker compose up -d
```

Migrations rodam sozinhas no start do backend.

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

backend:
```
docker compose exec backend pytest --cov=apps --cov-report=term-missing  # com cobertura
docker compose exec backend pytest  # sem cobertura
```

frontend:
```
cd frontend
npm run lint
npm run build
```

selenium:
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
