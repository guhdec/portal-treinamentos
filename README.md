# Portal de Treinamentos Audax

Portal web (React + Vite) que apresenta os treinamentos da rede de postos **Audax** como cursos navegáveis, com leitura por módulos, busca, acompanhamento de progresso e identidade visual da marca.

**No ar:** https://portal-treinamentos-eight.vercel.app
**Repositório:** https://github.com/guhdec/portal-treinamentos (branch `master`)

## Cursos

| Curso | ID | Conteúdo |
|-------|----|----------|
| **Gerentes de Postos 2026** | `postos` | Documentação regulatória e fiscalização — AVCB, Licença de Operação (CETESB), Alvará, Cadastro de Tanques e Bombas (IPEM), Laudo de Estanqueidade, Ficha ANP (6 módulos). |
| **Fluidos Automotivos** | `fluidos` | Treinamento para a gerência — Fluido de Freio (DOT 3/4), ATF, Óleos de Motor e Atendimento ao Cliente (4 módulos). |

O conteúdo foi transcrito dos documentos `.docx` originais para dados estruturados (ver "Modelo de conteúdo").

## Stack

- **React 19 + Vite** (SPA)
- **react-router-dom** — navegação Home → Curso → Módulo
- **Vitest + Testing Library** — testes de lógica e render
- CSS nativo com variáveis (sem framework), fonte **Poppins**

## Desenvolvimento

```bash
npm install
npm run dev      # servidor local (Vite)
npm test         # testes (Vitest)
npm run lint     # ESLint
npm run build    # build de produção em dist/
```

## Estrutura

```
src/
  main.jsx / App.jsx        # bootstrap + rotas
  index.css                 # tokens de design (cores Audax, fonte) + base
  data/
    schema.md               # esquema dos dados de curso
    courses/                # conteúdo: postos.js, fluidos.js, index.js
  hooks/useProgress.js      # progresso por módulo (localStorage)
  lib/search.js             # busca client-side (sem acento/caixa)
  components/               # Header, CourseCard, ModuleList, ModuleReader, blocks/...
  pages/                    # HomePage, CoursePage, ModulePage
public/
  img/                      # imagens dos cursos e logos
  favicon.ico, icon-192.png, apple-touch-icon.png   # favicon (A da Audax)
```

## Modelo de conteúdo

Cada curso é um objeto de dados (`src/data/courses/<curso>.js`) com `modulos`, e cada módulo tem `blocos` tipados: `titulo`, `paragrafo`, `lista`, `tabela`, `callout` (alerta/info/novidade), `pontos-chave` e `imagem`. Esquema completo em [`src/data/schema.md`](src/data/schema.md).

Para adicionar/editar conteúdo, basta editar os arquivos de dados — o teste `src/lib/courses.test.js` valida a integridade da estrutura.

## Identidade visual (Audax)

- **Cores:** vermelho `#F51115`, cinza `#575757`, acento ciano `#00C9DD`, branco.
- **Logo** no cabeçalho (versão branca sobre barra vermelha) e **favicon** com o símbolo "A".
- Acentos de marca (linha vermelho → ciano) em títulos e destaques.

As imagens em `public/img/` vêm de duas origens: renders do posto extraídos dos PDFs de marca Audax (uso interno) e fotos do **Unsplash** (licença livre) no curso de Fluidos.

## Progresso

A conclusão de cada módulo é salva no `localStorage` do navegador — individual por dispositivo, **sem login**. Não há backend.

## Deploy (Vercel)

- Projeto conectado ao GitHub `guhdec/portal-treinamentos`; **cada `git push` na `master` publica automaticamente**.
- Framework: Vite · Build: `npm run build` · Output: `dist`.
- `vercel.json` faz rewrite SPA para os deep links (ex.: `/curso/postos/modulo-2`) funcionarem.
