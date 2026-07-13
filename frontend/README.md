# Frontend

Aplicação React (Vite) do projeto To-Do List. Consome a API REST em `../backend`.

## Rodando localmente

```bash
npm install
cp .env.example .env
npm run dev
```

## Estrutura

```
src/
├── api/            # cliente axios e chamadas HTTP por recurso
├── components/     # componentes de UI reutilizáveis (layout, ui)
├── contexts/        # providers de estado global (ex.: autenticação)
├── features/        # regras de negócio e páginas por domínio (auth, tasks, categories, sharing)
├── hooks/           # hooks reutilizáveis
├── routes/           # definição de rotas e proteção de rotas privadas
├── styles/           # estilos globais
└── utils/            # constantes e helpers
```
