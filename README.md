# Portal de Treinamentos

Portal React+Vite com os treinamentos de Gerentes de Postos 2026 e Fluidos Automotivos.

## Desenvolvimento
- `npm install`
- `npm run dev` — servidor local
- `npm test` — testes (Vitest)
- `npm run build` — build de produção em `dist/`

## Deploy (Vercel)
- Framework: Vite. Build: `npm run build`. Output: `dist`.
- `vercel.json` faz rewrite SPA para deep links funcionarem.

O progresso de leitura é salvo no `localStorage` do navegador (individual por dispositivo, sem login).
