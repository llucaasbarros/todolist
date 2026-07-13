# Testes E2E (Selenium)

Testes de ponta a ponta que dirigem um Chrome real (via container `selenium/standalone-chrome`) contra a aplicação rodando em Docker.

## Rodando

Suba todos os serviços na raiz do projeto:

```bash
docker compose up -d
```

Instale as dependências (uma vez):

```bash
cd frontend/e2e
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Rode os testes:

```bash
.venv/bin/pytest -v
```

## Como funciona

- O Chrome roda dentro do container `selenium` (não no host — evita problemas de driver/bibliotecas do sistema).
- Os testes (rodando no host) controlam esse Chrome remotamente via `http://localhost:4444/wd/hub`.
- O Chrome navega até `http://frontend/` (nome do serviço, resolvido pela rede interna do Docker Compose).
- O bundle do frontend chama `http://localhost:8000/api` — dentro do container do Selenium isso apontaria para o próprio container, não pro backend. Por isso o `conftest.py` usa a flag `--host-resolver-rules` do Chrome pra redirecionar `localhost:8000` → `backend:8000` só na camada de rede, sem precisar rebuildar a imagem do frontend.
- Cada usuário de teste usa um username aleatório (`seluser_xxxxxxxx`) pra rodar múltiplas vezes sem conflito de "usuário já existe".
- Se um teste falhar, um screenshot é salvo em `screenshots/` (gitignored).

## Cobertura

- Registro + login (fluxo completo)
- Login com senha errada (mensagem de erro)
- Rota protegida redireciona pra `/login` sem sessão
- Logout redireciona pra `/login`
- Criar tarefa e ver na lista
- Marcar tarefa como concluída
- Excluir tarefa (incluindo o `window.confirm()` nativo)
