# To-Do List

Aplicação de gerenciamento de tarefas, feita como teste técnico. Backend em Django REST Framework, frontend em React, tudo rodando em containers Docker.

## Stack

Backend: Django 5.2, Django REST Framework, JWT (simplejwt), Postgres, pytest.
Frontend: React 18, Vite, react-router-dom, axios, CSS puro (sem Tailwind, sem lib de componentes).
Testes: pytest no backend (com cobertura), Selenium no frontend.
CI: GitHub Actions, lint com ruff no backend e eslint no frontend.

## Como rodar

Precisa ter Docker e Docker Compose instalados.

Clona o repositório e entra na pasta:

```
git clone <url-do-repo>
cd todolist
```

Copia os arquivos de variáveis de ambiente:

```
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Sobe tudo:

```
docker compose up -d
```

O backend aplica as migrations sozinho quando o container sobe (não precisa rodar nada manual). Depois de alguns segundos:

frontend: http://localhost:5183
backend / admin: http://localhost:8000/admin
api: http://localhost:8000/api

Pra acessar o admin precisa de um superusuário:

```
docker compose exec backend python src/manage.py createsuperuser
```

## Variáveis de ambiente

O `.env` da raiz define usuário e senha do Postgres que sobe no container `db`. O `backend/.env` usa essas mesmas credenciais pra conectar no banco. O `frontend/.env` só tem a URL da API, que já aponta pro backend em localhost:8000 por padrão.

## Testes

Backend, com cobertura:

```
docker compose exec backend pytest --cov=apps --cov-report=term-missing
```

Backend, sem cobertura:

```
docker compose exec backend pytest
```

Frontend, lint e build:

```
cd frontend
npm run lint
npm run build
```

Selenium, com a stack já no ar:

```
cd frontend/e2e
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/pytest -v
```

## Estrutura

Backend, apps separadas por domínio em `backend/src/apps/`:

- `core`: uma model abstrata (TimeStampedModel) reaproveitada pelas outras apps, não vira tabela própria.
- `accounts`: usuário customizado e os endpoints de registro e login.
- `categories`: CRUD de categorias, sempre isolado por dono.
- `tasks`: CRUD de tarefas, compartilhamento, filtro, paginação.
- `holidays`: integração com a BrasilAPI pra marcar quando o vencimento de uma tarefa cai num feriado nacional.

Frontend organizado por feature em `frontend/src/`:

- `api`: cliente axios e as chamadas HTTP por recurso.
- `features/<nome>/views`: as telas.
- `features/<nome>/components`: pedaços reutilizáveis dentro de cada feature.
- `components`: componentes genéricos usados em mais de uma feature (layout, paginação, toast).
- `contexts` e `hooks`: autenticação e outros estados globais.

## Decisões de design

- Usuário customizado desde o início (accounts.UserModel), pra não ter que migrar depois se precisar de campo extra.
- Isolamento por usuário no get_queryset de cada viewset, não só escondido no frontend. Categoria de outro usuário é rejeitada na validação do serializer.
- Compartilhamento de tarefa é só leitura, garantido por permission class no backend (IsOwnerOrReadOnly), não só por botão escondido na tela.
- Feriados nacionais via BrasilAPI, com cache de 24h, reaproveitado no serializer de tarefa pra marcar vencimento em feriado.
- Frontend sem biblioteca de UI, CSS puro com variáveis.
- Frontend em produção atrás de nginx, build multi-stage, com fallback de rota pro react-router.
- Selenium roda contra container selenium/standalone-chrome, sem precisar instalar Chrome e driver na máquina.
