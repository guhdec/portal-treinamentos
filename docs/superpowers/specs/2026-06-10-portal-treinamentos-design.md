# Portal de Treinamentos — Design

**Data:** 2026-06-10
**Status:** Aprovado para planejamento

## Objetivo

Construir um portal web que apresente dois treinamentos hoje em arquivos `.docx`, servindo tanto como **material de consulta** quanto como **treinamento** com acompanhamento de progresso. O site será publicado no **Vercel**.

Treinamentos:
1. **Gerentes de Postos 2026** — documentação regulatória e fiscalização (6 módulos: AVCB, CETESB/LO, Alvará, Cadastro de Tanques/IPEM, Laudo de Estanqueidade, Ficha ANP).
2. **Fluidos Automotivos** — para frentistas e gerentes (4 módulos: Fluido de Freio DOT 3/4, ATF, Óleos de Motor, Atendimento ao Cliente).

## Decisões tomadas

- **Stack:** React + Vite (aproveitando o scaffold existente).
- **Estrutura:** portal único listando os cursos; escalável para adicionar mais treinamentos.
- **Visual:** corporativo limpo — azul sóbrio, cinzas neutros, cards brancos, fonte sans legível.
- **Progresso:** marcar módulo como concluído, salvo em `localStorage` (sem login, sem backend).
- **Sem certificado.**
- **Deploy:** Vercel.
- **CSS:** variáveis CSS nativas (sem Tailwind), para manter leve.

## Arquitetura

### Modelo de conteúdo (dados separados da apresentação)

O conteúdo é autorado à mão como dados estruturados a partir do texto completo dos `.docx` (são apenas 2 documentos, de conteúdo fixo; um parser genérico achataria tabelas e caixas de destaque). A acentuação do texto de Fluidos será restaurada (o `.docx` original veio sem acentos).

Arquivos:
- `src/data/courses/postos.js`
- `src/data/courses/fluidos.js`
- `src/data/courses/index.js` — registra/exporta a lista de cursos (ponto único para adicionar treinamentos futuros).

Esquema:

```
Curso  = { id, titulo, subtitulo, descricaoCurta, icone, modulos: [Modulo] }
Modulo = { id, numero, titulo, resumo, blocos: [Bloco] }
Bloco  = um dos tipos:
  { tipo: "paragrafo", texto }
  { tipo: "titulo", nivel, texto }
  { tipo: "lista", itens: [string] }
  { tipo: "tabela", colunas: [string], linhas: [[string]] }
  { tipo: "callout", variante: "alerta" | "info" | "novidade", titulo?, texto | itens }
  { tipo: "pontos-chave", itens: [string] }   // "O QUE O GERENTE PRECISA SABER"
```

Os marcadores do material original mapeiam para `callout`:
- `⚠` → `variante: "alerta"`
- `ℹ` → `variante: "info"`
- `★ NOVIDADE` → `variante: "novidade"`
- `★ O QUE O GERENTE PRECISA SABER` → bloco `pontos-chave`

### Navegação (React Router)

Dependência nova: `react-router-dom`.

| Rota | Tela |
|------|------|
| `/` | Home do portal: cards dos cursos + busca global |
| `/curso/:cursoId` | Visão do curso: lista de módulos com % de progresso |
| `/curso/:cursoId/:moduloId` | Leitor do módulo + botão "marcar como concluído" |

Rota desconhecida → redireciona para `/`.

### Progresso

- Hook `useProgress` encapsula leitura/escrita em `localStorage`.
- Chave por módulo: `progresso:<cursoId>:<moduloId> = concluído (bool)`.
- Deriva: módulos concluídos por curso e % total do curso.
- Observação: o progresso é por navegador (individual de quem acessa), pois não há login.

### Busca

- Filtro client-side. Indexa título do curso, título/resumo dos módulos e texto dos blocos.
- Na Home, busca global retorna módulos correspondentes (com o curso de origem).

## Componentes

- `App` — define o roteamento.
- `Layout` / `Header` — cabeçalho do portal, navegação de volta à Home. (Candidato a geração via Magic MCP.)
- `HomePage` — grade de `CourseCard` + `SearchBox`.
- `CourseCard` — título, ícone, nº de módulos, % de progresso. (Candidato a Magic MCP.)
- `CoursePage` — cabeçalho do curso + `ModuleList`.
- `ModuleList` / `ModuleListItem` — módulos com ✓ de concluído.
- `ModulePage` / `ModuleReader` — renderiza os blocos do módulo + botão concluir + navegação anterior/próximo.
- Renderizadores de bloco: `Paragraph`, `Heading`, `BulletList`, `DataTable`, `Callout`, `KeyPoints`.
- `ProgressBar` — barra de % reutilizável.
- `SearchBox` — input de busca.
- `useProgress` — hook de progresso.

## Estilo visual

- Tokens CSS em `src/index.css` (`:root`): cores, espaçamentos, raio de borda, sombras.
  - Primária azul `#1e3a5f`; acento `#2563eb`; neutros cinza; fundo claro; cards brancos.
  - Variantes de callout: alerta (âmbar/vermelho), info (azul claro), novidade (verde/destaque).
- Layout responsivo (mobile-first), legível, espaçamento generoso.
- Sem framework CSS; CSS por componente (CSS Modules ou arquivos `.css` co-localizados).

## Deploy

- `vercel.json` com rewrite SPA (`/* → /index.html`) para deep links funcionarem.
- Build: `vite build` → `dist/`.

## Limpeza

- Remover o conteúdo do template padrão: reescrever `src/App.jsx`, remover `src/assets/hero.png`, `react.svg`, `vite.svg` de exemplo e estilos não usados; ajustar `index.html` (`<title>` e `lang="pt-BR"`).
- Os arquivos legados `generate_html.py` e `extracted_content.json` não serão usados; manter no repositório (fora do build) ou remover — decidir no plano.

## Fora de escopo (YAGNI)

- Login / contas de usuário.
- Certificado.
- Backend / banco de dados.
- Geração automática a partir dos `.docx` em runtime (conteúdo é autorado uma vez).
- Quiz/avaliações (não solicitado nesta etapa).

## Critérios de sucesso

- Home lista os 2 cursos com progresso visível.
- É possível abrir qualquer módulo, ler o conteúdo (tabelas e callouts renderizados corretamente) e marcar como concluído; o progresso persiste após recarregar.
- Busca encontra módulos por palavra-chave.
- Deep links (ex.: `/curso/postos/modulo-2`) funcionam após deploy no Vercel.
- `npm run build` conclui sem erros; `npm run lint` limpo.
