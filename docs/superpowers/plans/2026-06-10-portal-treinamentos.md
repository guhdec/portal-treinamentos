# Portal de Treinamentos — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Construir um portal React+Vite que apresente 2 treinamentos (hoje em `.docx`) como cursos navegáveis, com leitura de módulos, busca e progresso por `localStorage`, publicável no Vercel.

**Architecture:** Conteúdo autorado como dados estruturados em `src/data/`, separado da apresentação. React Router para Home → Curso → Módulo. Hook `useProgress` persiste conclusão em `localStorage`. Renderizadores de bloco transformam o modelo de conteúdo (parágrafo, lista, tabela, callout, pontos-chave) em UI corporativa limpa via CSS com variáveis.

**Tech Stack:** React 19, Vite, react-router-dom, Vitest + @testing-library/react (jsdom), CSS nativo com variáveis.

**Referência:** spec em `docs/superpowers/specs/2026-06-10-portal-treinamentos-design.md`.

---

## File Structure

```
index.html                         # title + lang pt-BR
vercel.json                        # rewrite SPA
src/
  main.jsx                         # monta <App/> com BrowserRouter
  App.jsx                          # rotas
  index.css                        # tokens de design (:root) + base
  data/
    courses/
      index.js                     # lista de cursos (getCourses, getCourse, getModule)
      postos.js                    # curso "postos" (6 módulos)
      fluidos.js                   # curso "fluidos" (4 módulos)
    schema.md                      # documentação do esquema de dados
  hooks/
    useProgress.js                 # progresso via localStorage
    useProgress.test.js
  lib/
    search.js                      # busca client-side
    search.test.js
    courses.test.js                # teste de integridade dos dados
  components/
    Layout.jsx        Layout.css
    Header.jsx        Header.css
    CourseCard.jsx    CourseCard.css
    ProgressBar.jsx   ProgressBar.css
    SearchBox.jsx     SearchBox.css
    ModuleList.jsx    ModuleList.css
    ModuleReader.jsx  ModuleReader.css
    blocks/
      BlockRenderer.jsx            # despacha por tipo
      Callout.jsx     Callout.css
      DataTable.jsx   DataTable.css
      KeyPoints.jsx   KeyPoints.css
      Heading.jsx  Paragraph.jsx  BulletList.jsx   (+ blocks.css compartilhado)
  pages/
    HomePage.jsx      HomePage.css
    CoursePage.jsx    CoursePage.css
    ModulePage.jsx    ModulePage.css
```

---

## Task 0: Setup do projeto, ferramentas e git

**Files:**
- Modify: `package.json`
- Create: `vitest.config.js`, `src/test/setup.js`
- Modify: `index.html`

- [ ] **Step 1: Inicializar git**

Run:
```bash
git init && git add -A && git commit -m "chore: scaffold inicial (template Vite)"
```
Expected: repositório criado com o estado atual commitado.

- [ ] **Step 2: Instalar dependências**

Run:
```bash
npm install react-router-dom
npm install -D vitest @testing-library/react @testing-library/jest-dom jsdom
```
Expected: pacotes adicionados sem erro.

- [ ] **Step 3: Adicionar script de teste em `package.json`**

No bloco `"scripts"`, adicionar:
```json
"test": "vitest run",
"test:watch": "vitest"
```

- [ ] **Step 4: Criar `vitest.config.js`**

```js
import { defineConfig } from 'vitest/config'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: ['./src/test/setup.js'],
  },
})
```

- [ ] **Step 5: Criar `src/test/setup.js`**

```js
import '@testing-library/jest-dom'
```

- [ ] **Step 6: Ajustar `index.html`**

Trocar `lang="en"` por `lang="pt-BR"` e o `<title>` para `Portal de Treinamentos`.

- [ ] **Step 7: Verificar que a suíte roda (vazia)**

Run: `npm test`
Expected: Vitest executa e reporta "no test files" (sem erro de configuração).

- [ ] **Step 8: Commit**

```bash
git add -A && git commit -m "chore: configurar router, vitest e ajustes de index.html"
```

---

## Task 1: Modelo de conteúdo — esquema e índice de cursos

Define o esquema, o índice de acesso aos dados e um teste de integridade. O conteúdo real é transcrito na Task 2.

**Files:**
- Create: `src/data/schema.md`
- Create: `src/data/courses/index.js`
- Create: `src/data/courses/postos.js` (stub mínimo nesta task)
- Create: `src/data/courses/fluidos.js` (stub mínimo nesta task)
- Test: `src/lib/courses.test.js`

- [ ] **Step 1: Documentar o esquema em `src/data/schema.md`**

```markdown
# Esquema de dados de cursos

Curso  = { id, titulo, subtitulo, descricaoCurta, icone, modulos: [Modulo] }
Modulo = { id, numero, titulo, resumo, blocos: [Bloco] }

Bloco (campo `tipo` discrimina):
- { tipo: "titulo", nivel: 2|3, texto }
- { tipo: "paragrafo", texto }
- { tipo: "lista", itens: [string] }
- { tipo: "tabela", colunas: [string], linhas: [[string]] }
- { tipo: "callout", variante: "alerta"|"info"|"novidade", titulo?, texto?, itens?: [string] }
- { tipo: "pontos-chave", itens: [string] }   // "O QUE O GERENTE PRECISA SABER"

Regras:
- id de curso e de módulo são kebab-case, únicos.
- módulos usam id "modulo-N" (N = numero).
- `icone`: string curta (emoji) usada nos cards.
```

- [ ] **Step 2: Escrever o teste de integridade `src/lib/courses.test.js`**

```js
import { describe, it, expect } from 'vitest'
import { getCourses, getCourse, getModule } from '../data/courses/index.js'

const TIPOS = new Set(['titulo', 'paragrafo', 'lista', 'tabela', 'callout', 'pontos-chave'])

describe('catálogo de cursos', () => {
  it('expõe os dois cursos esperados', () => {
    const ids = getCourses().map((c) => c.id).sort()
    expect(ids).toEqual(['fluidos', 'postos'])
  })

  it('cada curso tem campos obrigatórios e módulos', () => {
    for (const curso of getCourses()) {
      expect(curso.titulo).toBeTruthy()
      expect(curso.icone).toBeTruthy()
      expect(Array.isArray(curso.modulos)).toBe(true)
      expect(curso.modulos.length).toBeGreaterThan(0)
    }
  })

  it('ids de módulo são únicos e blocos têm tipos válidos', () => {
    for (const curso of getCourses()) {
      const ids = curso.modulos.map((m) => m.id)
      expect(new Set(ids).size).toBe(ids.length)
      for (const m of curso.modulos) {
        expect(m.titulo).toBeTruthy()
        for (const b of m.blocos) {
          expect(TIPOS.has(b.tipo)).toBe(true)
          if (b.tipo === 'tabela') {
            for (const linha of b.linhas) {
              expect(linha.length).toBe(b.colunas.length)
            }
          }
        }
      }
    }
  })

  it('getCourse e getModule resolvem por id', () => {
    const curso = getCourse('postos')
    expect(curso.id).toBe('postos')
    const mod = getModule('postos', curso.modulos[0].id)
    expect(mod).toBeTruthy()
    expect(getModule('postos', 'inexistente')).toBeUndefined()
    expect(getCourse('inexistente')).toBeUndefined()
  })
})
```

- [ ] **Step 3: Criar stubs de dados para o teste falhar de forma significativa**

`src/data/courses/postos.js`:
```js
export const postos = {
  id: 'postos',
  titulo: 'Gerentes de Postos 2026',
  subtitulo: 'Documentação regulatória e fiscalização',
  descricaoCurta: 'Documentos exigidos pelos órgãos fiscalizadores e conduta em vistorias.',
  icone: '⛽',
  modulos: [
    {
      id: 'modulo-1',
      numero: 1,
      titulo: 'AVCB — Corpo de Bombeiros',
      resumo: 'Auto de Vistoria do Corpo de Bombeiros (CBPMESP).',
      blocos: [
        { tipo: 'paragrafo', texto: 'Conteúdo a transcrever na Task 2.' },
      ],
    },
  ],
}
```

`src/data/courses/fluidos.js`:
```js
export const fluidos = {
  id: 'fluidos',
  titulo: 'Fluidos Automotivos',
  subtitulo: 'Para frentistas e gerentes',
  descricaoCurta: 'Fluido de freio, ATF, óleos de motor e atendimento ao cliente.',
  icone: '🛢️',
  modulos: [
    {
      id: 'modulo-1',
      numero: 1,
      titulo: 'Fluido de Freio: DOT 3 e DOT 4',
      resumo: 'Função, especificação DOT e cuidados.',
      blocos: [
        { tipo: 'paragrafo', texto: 'Conteúdo a transcrever na Task 2.' },
      ],
    },
  ],
}
```

- [ ] **Step 4: Criar `src/data/courses/index.js`**

```js
import { postos } from './postos.js'
import { fluidos } from './fluidos.js'

const CURSOS = [postos, fluidos]

export function getCourses() {
  return CURSOS
}

export function getCourse(cursoId) {
  return CURSOS.find((c) => c.id === cursoId)
}

export function getModule(cursoId, moduloId) {
  return getCourse(cursoId)?.modulos.find((m) => m.id === moduloId)
}
```

- [ ] **Step 5: Rodar o teste**

Run: `npm test src/lib/courses.test.js`
Expected: PASS (estrutura válida com os stubs).

- [ ] **Step 6: Commit**

```bash
git add -A && git commit -m "feat(data): esquema, índice de cursos e teste de integridade"
```

---

## Task 2: Transcrever o conteúdo completo dos dois cursos

Substitui os stubs pelo conteúdo real, extraído na íntegra dos `.docx`. Esta é a transcrição fiel do material (o texto é a fonte de verdade), seguindo o esquema. **Restaurar a acentuação correta** no curso de Fluidos.

**Files:**
- Modify: `src/data/courses/postos.js` (6 módulos completos)
- Modify: `src/data/courses/fluidos.js` (4 módulos completos)

- [ ] **Step 1: Extrair o texto integral dos dois `.docx`**

Run (extrai todo o texto, sem truncar):
```bash
for f in "Treinamento_Gerentes_Postos_2026.docx" "treinamento-fluidos-v2.docx"; do \
  echo "=== $f ==="; \
  unzip -p "$f" word/document.xml | tr '<' '\n' | grep -oP '(?<=>)[^<]+'; \
done > /tmp/treinamento_full.txt
```
Expected: arquivo com o texto completo dos 6 módulos de Postos e 4 de Fluidos (inclui Módulos 5 e 6 de Postos não vistos no preview).

- [ ] **Step 2: Transcrever `postos.js` (Módulos 1–6)**

Para cada módulo, mapear o material para blocos do esquema:
- Títulos de seção (ex.: "O que é?", "Base Legal Vigente em 2026") → `{ tipo: 'titulo', nivel: 3, texto }`.
- Texto corrido → `{ tipo: 'paragrafo', texto }`.
- Tabelas "Norma / O que regula", modalidades, consequências → `{ tipo: 'tabela', colunas, linhas }`.
- Caixas `⚠` → `callout` variante `alerta`; `ℹ` → `info`; `★ NOVIDADE` → `novidade` (com `titulo`).
- Listas com marcadores → `{ tipo: 'lista', itens }`.
- "★ O QUE O GERENTE PRECISA SABER" → `{ tipo: 'pontos-chave', itens }`.

Módulos e ids:
`modulo-1` AVCB · `modulo-2` Licença de Operação (CETESB) · `modulo-3` Alvará de Funcionamento · `modulo-4` Cadastro de Tanques e Bombas (IPEM) · `modulo-5` Laudo de Estanqueidade · `modulo-6` Ficha ANP / Autorização de Funcionamento.

Exemplo de um módulo já mapeado (padrão a seguir para todos):
```js
{
  id: 'modulo-1',
  numero: 1,
  titulo: 'AVCB — Corpo de Bombeiros',
  resumo: 'Auto de Vistoria do Corpo de Bombeiros (CBPMESP) para área de alto risco.',
  blocos: [
    { tipo: 'titulo', nivel: 3, texto: 'O que é?' },
    { tipo: 'paragrafo', texto: 'O AVCB é o documento emitido pelo Corpo de Bombeiros Militar do Estado de São Paulo (CBPMESP) após vistoria técnica presencial, certificando que o estabelecimento atende às exigências de segurança contra incêndio e pânico. Para postos de combustíveis — classificados como área de alto risco — o AVCB é obrigatório, não podendo ser substituído pelo CLCB (destinado apenas a atividades de baixo risco).' },
    { tipo: 'titulo', nivel: 3, texto: 'Base Legal Vigente em 2026' },
    {
      tipo: 'tabela',
      colunas: ['Norma', 'O que regula'],
      linhas: [
        ['Lei Federal nº 13.425/2017 (Lei Kiss)', 'Vincula o alvará de funcionamento ao licenciamento do Corpo de Bombeiros.'],
        ['Decreto Estadual SP nº 69.118/2024', 'Novo Regulamento de Segurança Contra Incêndios — em vigor desde dezembro de 2024. Revoga e substitui o Decreto 63.911/2018.'],
        ['ITs do CBPMESP (2025/2026)', 'Instruções Técnicas atualizadas: IT-02 (saídas), IT-16 (hidrantes), IT-25 (tanques inflamáveis), IT-28 (GNV). Consultar versões vigentes no site do CBPMESP.'],
      ],
    },
    {
      tipo: 'callout',
      variante: 'novidade',
      titulo: 'NOVIDADE 2025/2026 — Decreto nº 69.118/2024 em vigor',
      texto: 'O novo regulamento, publicado em dezembro de 2024 e plenamente vigente em 2026, adota critérios mais claros para aprovação de projetos, procedimentos mais objetivos para regularização de edificações existentes e define responsabilidades técnicas de projetistas, executores e proprietários. Projetos iniciados sob o decreto anterior devem ser adequados às novas regras.',
    },
    {
      tipo: 'callout',
      variante: 'info',
      titulo: 'Validade do AVCB em 2026',
      texto: 'Conforme o Decreto nº 69.118/2024, a validade varia de 1 a 5 anos dependendo das características da edificação e do nível de risco. Renovação pelo portal Via Fácil Bombeiro (viafacil.bombeiros.sp.gov.br). Sem o AVCB vigente, o Alvará de Funcionamento da Prefeitura não pode ser emitido ou renovado.',
    },
    {
      tipo: 'pontos-chave',
      itens: [
        'AVCB é obrigatório para posto. Não existe modalidade simplificada (CLCB) para atividades de alto risco como combustíveis.',
        'Validade de 1 a 5 anos — verifique a data de vencimento antes de qualquer época de renovação.',
        'O AVCB deve estar fisicamente no posto, de fácil acesso. Nunca diga "está com o contador".',
        'Desde dezembro de 2024, o Decreto nº 69.118/2024 está em vigor. Se o AVCB foi emitido sob decreto anterior e for renovar, o projeto pode precisar de adequações.',
        'Sem AVCB, não há Alvará da Prefeitura. Os documentos são encadeados.',
        'Nunca rompa lacre ou interdição do Corpo de Bombeiros — é crime.',
      ],
    },
  ],
}
```

- [ ] **Step 3: Transcrever `fluidos.js` (Módulos 1–4) com acentuação corrigida**

ids: `modulo-1` Fluido de Freio (DOT 3/4) · `modulo-2` ATF · `modulo-3` Óleos de Motor · `modulo-4` Atendimento e Orientação ao Cliente. Incluir o bloco inicial "Regra de Ouro" como `callout` variante `alerta` no `modulo-1` (ou em um resumo do curso, à escolha — manter no modulo-1). Tabelas comparativas (DOT 3 × DOT 4, comparativo dos óleos, situações de atendimento) viram `tabela`. Corrigir acentos (ex.: "função", "freio", "veículo", "óleo").

- [ ] **Step 4: Rodar o teste de integridade**

Run: `npm test src/lib/courses.test.js`
Expected: PASS (tabelas com nº de colunas consistente, tipos válidos, ids únicos).

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat(data): transcrever conteúdo completo dos cursos postos e fluidos"
```

---

## Task 3: Hook de progresso (`useProgress`) — TDD

**Files:**
- Create: `src/hooks/useProgress.js`
- Test: `src/hooks/useProgress.test.js`

- [ ] **Step 1: Escrever os testes**

```js
import { describe, it, expect, beforeEach } from 'vitest'
import { renderHook, act } from '@testing-library/react'
import { useProgress } from './useProgress.js'

beforeEach(() => localStorage.clear())

describe('useProgress', () => {
  it('inicia sem módulos concluídos', () => {
    const { result } = renderHook(() => useProgress('postos'))
    expect(result.current.isDone('modulo-1')).toBe(false)
    expect(result.current.completedCount).toBe(0)
  })

  it('marca e desmarca um módulo, persistindo em localStorage', () => {
    const { result } = renderHook(() => useProgress('postos'))
    act(() => result.current.toggle('modulo-1'))
    expect(result.current.isDone('modulo-1')).toBe(true)
    expect(result.current.completedCount).toBe(1)
    expect(localStorage.getItem('progresso:postos:modulo-1')).toBe('1')
    act(() => result.current.toggle('modulo-1'))
    expect(result.current.isDone('modulo-1')).toBe(false)
    expect(localStorage.getItem('progresso:postos:modulo-1')).toBeNull()
  })

  it('isola o progresso por curso', () => {
    const { result: postos } = renderHook(() => useProgress('postos'))
    act(() => postos.current.toggle('modulo-1'))
    const { result: fluidos } = renderHook(() => useProgress('fluidos'))
    expect(fluidos.current.isDone('modulo-1')).toBe(false)
  })

  it('calcula percent a partir do total informado', () => {
    const { result } = renderHook(() => useProgress('postos'))
    act(() => result.current.toggle('modulo-1'))
    act(() => result.current.toggle('modulo-2'))
    expect(result.current.percent(4)).toBe(50)
  })
})
```

- [ ] **Step 2: Rodar e ver falhar**

Run: `npm test src/hooks/useProgress.test.js`
Expected: FAIL ("does not provide an export named 'useProgress'").

- [ ] **Step 3: Implementar `src/hooks/useProgress.js`**

```js
import { useState, useCallback } from 'react'

const key = (cursoId, moduloId) => `progresso:${cursoId}:${moduloId}`

function readDone(cursoId) {
  const prefix = `progresso:${cursoId}:`
  const done = new Set()
  for (let i = 0; i < localStorage.length; i++) {
    const k = localStorage.key(i)
    if (k && k.startsWith(prefix) && localStorage.getItem(k) === '1') {
      done.add(k.slice(prefix.length))
    }
  }
  return done
}

export function useProgress(cursoId) {
  const [done, setDone] = useState(() => readDone(cursoId))

  const toggle = useCallback(
    (moduloId) => {
      setDone((prev) => {
        const next = new Set(prev)
        if (next.has(moduloId)) {
          next.delete(moduloId)
          localStorage.removeItem(key(cursoId, moduloId))
        } else {
          next.add(moduloId)
          localStorage.setItem(key(cursoId, moduloId), '1')
        }
        return next
      })
    },
    [cursoId],
  )

  const isDone = useCallback((moduloId) => done.has(moduloId), [done])
  const percent = useCallback(
    (total) => (total === 0 ? 0 : Math.round((done.size / total) * 100)),
    [done],
  )

  return { isDone, toggle, percent, completedCount: done.size }
}
```

- [ ] **Step 4: Rodar e ver passar**

Run: `npm test src/hooks/useProgress.test.js`
Expected: PASS (4 testes).

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat(hooks): useProgress com persistência em localStorage"
```

---

## Task 4: Busca client-side (`search`) — TDD

**Files:**
- Create: `src/lib/search.js`
- Test: `src/lib/search.test.js`

- [ ] **Step 1: Escrever os testes**

```js
import { describe, it, expect } from 'vitest'
import { searchModules } from './search.js'

describe('searchModules', () => {
  it('retorna vazio para query em branco', () => {
    expect(searchModules('   ')).toEqual([])
  })

  it('encontra módulo por palavra no título (case/acento-insensível)', () => {
    const r = searchModules('avcb')
    expect(r.some((x) => x.modulo.id === 'modulo-1' && x.curso.id === 'postos')).toBe(true)
  })

  it('encontra por texto no conteúdo dos blocos', () => {
    const r = searchModules('estanqueidade')
    expect(r.length).toBeGreaterThan(0)
    expect(r[0]).toHaveProperty('curso')
    expect(r[0]).toHaveProperty('modulo')
  })

  it('ignora acentos na query', () => {
    const r = searchModules('oleo')
    expect(r.some((x) => x.curso.id === 'fluidos')).toBe(true)
  })
})
```

- [ ] **Step 2: Rodar e ver falhar**

Run: `npm test src/lib/search.test.js`
Expected: FAIL ("does not provide an export named 'searchModules'").

- [ ] **Step 3: Implementar `src/lib/search.js`**

```js
import { getCourses } from '../data/courses/index.js'

const norm = (s) =>
  s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase()

function moduloTexto(m) {
  const partes = [m.titulo, m.resumo || '']
  for (const b of m.blocos) {
    if (b.texto) partes.push(b.texto)
    if (b.itens) partes.push(b.itens.join(' '))
    if (b.colunas) partes.push(b.colunas.join(' '))
    if (b.linhas) partes.push(b.linhas.flat().join(' '))
  }
  return norm(partes.join(' '))
}

export function searchModules(query) {
  const q = norm(query.trim())
  if (!q) return []
  const out = []
  for (const curso of getCourses()) {
    for (const modulo of curso.modulos) {
      if (moduloTexto(modulo).includes(q)) out.push({ curso, modulo })
    }
  }
  return out
}
```

- [ ] **Step 4: Rodar e ver passar**

Run: `npm test src/lib/search.test.js`
Expected: PASS (4 testes).

- [ ] **Step 5: Commit**

```bash
git add -A && git commit -m "feat(lib): busca client-side de módulos sem acento/caixa"
```

---

## Task 5: Tokens de design e base CSS

**Files:**
- Modify: `src/index.css` (substituir conteúdo do template)

- [ ] **Step 1: Substituir `src/index.css`**

```css
:root {
  /* cores */
  --azul-900: #1e3a5f;
  --azul-700: #274b78;
  --azul-500: #2563eb;
  --cinza-50: #f6f8fa;
  --cinza-100: #eef1f5;
  --cinza-200: #dde3ea;
  --cinza-500: #64748b;
  --cinza-700: #334155;
  --cinza-900: #0f172a;
  --branco: #ffffff;
  /* callouts */
  --alerta-bg: #fef3f2; --alerta-borda: #d92d20; --alerta-txt: #7a271a;
  --info-bg: #eff6ff;   --info-borda: #2563eb;   --info-txt: #1e3a5f;
  --novidade-bg: #ecfdf3; --novidade-borda: #12b76a; --novidade-txt: #054f31;
  /* layout */
  --raio: 10px;
  --sombra: 0 1px 3px rgba(15,23,42,.08), 0 1px 2px rgba(15,23,42,.06);
  --max-largura: 980px;
  --gap: 1rem;
  font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif;
  color: var(--cinza-900);
}

* { box-sizing: border-box; }
body { margin: 0; background: var(--cinza-50); line-height: 1.6; }
a { color: var(--azul-500); text-decoration: none; }
a:hover { text-decoration: underline; }
h1, h2, h3 { color: var(--azul-900); line-height: 1.25; }
.container { max-width: var(--max-largura); margin: 0 auto; padding: 1.5rem 1rem 4rem; }
```

- [ ] **Step 2: Verificar build (sanidade)**

Run: `npm run build`
Expected: build conclui (App ainda é o template — ok nesta task).

- [ ] **Step 3: Commit**

```bash
git add -A && git commit -m "style: tokens de design corporativo e base css"
```

---

## Task 6: Renderizadores de bloco

Componentes de apresentação puros (sem estado). Verificação por build + smoke test de despacho.

**Files:**
- Create: `src/components/blocks/BlockRenderer.jsx`
- Create: `src/components/blocks/Callout.jsx` + `Callout.css`
- Create: `src/components/blocks/DataTable.jsx` + `DataTable.css`
- Create: `src/components/blocks/KeyPoints.jsx` + `KeyPoints.css`
- Create: `src/components/blocks/Heading.jsx`, `Paragraph.jsx`, `BulletList.jsx`, `blocks.css`
- Test: `src/components/blocks/BlockRenderer.test.jsx`

- [ ] **Step 1: Escrever smoke test do despacho**

```jsx
import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BlockRenderer } from './BlockRenderer.jsx'

describe('BlockRenderer', () => {
  it('renderiza parágrafo', () => {
    render(<BlockRenderer bloco={{ tipo: 'paragrafo', texto: 'Olá mundo' }} />)
    expect(screen.getByText('Olá mundo')).toBeInTheDocument()
  })
  it('renderiza tabela com cabeçalhos e células', () => {
    render(<BlockRenderer bloco={{ tipo: 'tabela', colunas: ['A', 'B'], linhas: [['1', '2']] }} />)
    expect(screen.getByText('A')).toBeInTheDocument()
    expect(screen.getByText('2')).toBeInTheDocument()
  })
  it('renderiza callout com título', () => {
    render(<BlockRenderer bloco={{ tipo: 'callout', variante: 'alerta', titulo: 'Atenção', texto: 'cuidado' }} />)
    expect(screen.getByText('Atenção')).toBeInTheDocument()
    expect(screen.getByText('cuidado')).toBeInTheDocument()
  })
  it('renderiza pontos-chave', () => {
    render(<BlockRenderer bloco={{ tipo: 'pontos-chave', itens: ['ponto um'] }} />)
    expect(screen.getByText('ponto um')).toBeInTheDocument()
  })
})
```

- [ ] **Step 2: Rodar e ver falhar**

Run: `npm test src/components/blocks/BlockRenderer.test.jsx`
Expected: FAIL (módulo não existe).

- [ ] **Step 3: Implementar os blocos simples (`Heading.jsx`, `Paragraph.jsx`, `BulletList.jsx`)**

`Heading.jsx`:
```jsx
export function Heading({ nivel = 3, texto }) {
  const Tag = nivel === 2 ? 'h2' : 'h3'
  return <Tag className="bloco-titulo">{texto}</Tag>
}
```
`Paragraph.jsx`:
```jsx
export function Paragraph({ texto }) {
  return <p className="bloco-paragrafo">{texto}</p>
}
```
`BulletList.jsx`:
```jsx
export function BulletList({ itens }) {
  return (
    <ul className="bloco-lista">
      {itens.map((it, i) => <li key={i}>{it}</li>)}
    </ul>
  )
}
```
`blocks.css`:
```css
.bloco-titulo { margin: 1.75rem 0 .5rem; }
.bloco-paragrafo { margin: .5rem 0; color: var(--cinza-700); }
.bloco-lista { margin: .5rem 0; padding-left: 1.25rem; color: var(--cinza-700); }
.bloco-lista li { margin: .25rem 0; }
```

- [ ] **Step 4: Implementar `Callout.jsx` + `Callout.css`**

```jsx
import './Callout.css'

const ICONE = { alerta: '⚠', info: 'ℹ', novidade: '★' }

export function Callout({ variante = 'info', titulo, texto, itens }) {
  return (
    <div className={`callout callout--${variante}`} role="note">
      <div className="callout__cabecalho">
        <span className="callout__icone" aria-hidden="true">{ICONE[variante]}</span>
        {titulo && <strong className="callout__titulo">{titulo}</strong>}
      </div>
      {texto && <p className="callout__texto">{texto}</p>}
      {itens && (
        <ul className="callout__lista">
          {itens.map((it, i) => <li key={i}>{it}</li>)}
        </ul>
      )}
    </div>
  )
}
```
```css
.callout { border-left: 4px solid; border-radius: var(--raio); padding: .75rem 1rem; margin: 1rem 0; }
.callout__cabecalho { display: flex; align-items: center; gap: .5rem; }
.callout__icone { font-size: 1.1rem; }
.callout__texto, .callout__lista { margin: .5rem 0 0; }
.callout--alerta   { background: var(--alerta-bg);   border-color: var(--alerta-borda);   color: var(--alerta-txt); }
.callout--info     { background: var(--info-bg);     border-color: var(--info-borda);     color: var(--info-txt); }
.callout--novidade { background: var(--novidade-bg); border-color: var(--novidade-borda); color: var(--novidade-txt); }
```

- [ ] **Step 5: Implementar `DataTable.jsx` + `DataTable.css`**

```jsx
import './DataTable.css'

export function DataTable({ colunas, linhas }) {
  return (
    <div className="tabela-wrap">
      <table className="tabela">
        <thead>
          <tr>{colunas.map((c, i) => <th key={i}>{c}</th>)}</tr>
        </thead>
        <tbody>
          {linhas.map((linha, r) => (
            <tr key={r}>{linha.map((cel, c) => <td key={c}>{cel}</td>)}</tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
```
```css
.tabela-wrap { overflow-x: auto; margin: 1rem 0; }
.tabela { width: 100%; border-collapse: collapse; background: var(--branco); border-radius: var(--raio); overflow: hidden; box-shadow: var(--sombra); }
.tabela th, .tabela td { text-align: left; padding: .6rem .8rem; border-bottom: 1px solid var(--cinza-200); vertical-align: top; }
.tabela th { background: var(--azul-900); color: var(--branco); font-weight: 600; }
.tabela tr:last-child td { border-bottom: none; }
.tabela tbody tr:nth-child(even) { background: var(--cinza-50); }
```

- [ ] **Step 6: Implementar `KeyPoints.jsx` + `KeyPoints.css`**

```jsx
import './KeyPoints.css'

export function KeyPoints({ itens }) {
  return (
    <div className="pontos-chave">
      <h3 className="pontos-chave__titulo">★ O que você precisa saber</h3>
      <ol className="pontos-chave__lista">
        {itens.map((it, i) => <li key={i}>{it}</li>)}
      </ol>
    </div>
  )
}
```
```css
.pontos-chave { background: var(--cinza-100); border-radius: var(--raio); padding: 1rem 1.25rem; margin: 1.5rem 0; }
.pontos-chave__titulo { margin: 0 0 .5rem; }
.pontos-chave__lista { margin: 0; padding-left: 1.25rem; }
.pontos-chave__lista li { margin: .4rem 0; color: var(--cinza-700); }
```

- [ ] **Step 7: Implementar `BlockRenderer.jsx`**

```jsx
import './blocks.css'
import { Heading } from './Heading.jsx'
import { Paragraph } from './Paragraph.jsx'
import { BulletList } from './BulletList.jsx'
import { Callout } from './Callout.jsx'
import { DataTable } from './DataTable.jsx'
import { KeyPoints } from './KeyPoints.jsx'

export function BlockRenderer({ bloco }) {
  switch (bloco.tipo) {
    case 'titulo':       return <Heading nivel={bloco.nivel} texto={bloco.texto} />
    case 'paragrafo':    return <Paragraph texto={bloco.texto} />
    case 'lista':        return <BulletList itens={bloco.itens} />
    case 'tabela':       return <DataTable colunas={bloco.colunas} linhas={bloco.linhas} />
    case 'callout':      return <Callout {...bloco} />
    case 'pontos-chave': return <KeyPoints itens={bloco.itens} />
    default:             return null
  }
}
```

- [ ] **Step 8: Rodar e ver passar**

Run: `npm test src/components/blocks/BlockRenderer.test.jsx`
Expected: PASS (4 testes).

- [ ] **Step 9: Commit**

```bash
git add -A && git commit -m "feat(blocks): renderizadores de parágrafo, lista, tabela, callout e pontos-chave"
```

---

## Task 7: Componentes compartilhados (ProgressBar, SearchBox, CourseCard, Header, Layout)

**Files:**
- Create: `src/components/ProgressBar.jsx` + `ProgressBar.css`
- Create: `src/components/SearchBox.jsx` + `SearchBox.css`
- Create: `src/components/CourseCard.jsx` + `CourseCard.css`
- Create: `src/components/Header.jsx` + `Header.css`
- Create: `src/components/Layout.jsx` + `Layout.css`

- [ ] **Step 1: `ProgressBar.jsx` + `ProgressBar.css`**

```jsx
import './ProgressBar.css'

export function ProgressBar({ percent, label }) {
  return (
    <div className="progresso">
      <div className="progresso__trilho">
        <div className="progresso__barra" style={{ width: `${percent}%` }} />
      </div>
      <span className="progresso__rotulo">{label ?? `${percent}%`}</span>
    </div>
  )
}
```
```css
.progresso { display: flex; align-items: center; gap: .5rem; }
.progresso__trilho { flex: 1; height: 8px; background: var(--cinza-200); border-radius: 999px; overflow: hidden; }
.progresso__barra { height: 100%; background: var(--azul-500); transition: width .25s ease; }
.progresso__rotulo { font-size: .8rem; color: var(--cinza-500); min-width: 3.5rem; text-align: right; }
```

- [ ] **Step 2: `SearchBox.jsx` + `SearchBox.css`**

```jsx
import './SearchBox.css'

export function SearchBox({ valor, onChange, placeholder = 'Buscar nos treinamentos…' }) {
  return (
    <input
      type="search"
      className="busca"
      value={valor}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      aria-label="Buscar"
    />
  )
}
```
```css
.busca { width: 100%; padding: .7rem 1rem; border: 1px solid var(--cinza-200); border-radius: var(--raio); font-size: 1rem; background: var(--branco); }
.busca:focus { outline: 2px solid var(--azul-500); border-color: var(--azul-500); }
```

- [ ] **Step 3: `CourseCard.jsx` + `CourseCard.css`**

```jsx
import { Link } from 'react-router-dom'
import { ProgressBar } from './ProgressBar.jsx'
import { useProgress } from '../hooks/useProgress.js'
import './CourseCard.css'

export function CourseCard({ curso }) {
  const { percent } = useProgress(curso.id)
  const total = curso.modulos.length
  return (
    <Link to={`/curso/${curso.id}`} className="curso-card">
      <span className="curso-card__icone" aria-hidden="true">{curso.icone}</span>
      <h2 className="curso-card__titulo">{curso.titulo}</h2>
      <p className="curso-card__subtitulo">{curso.subtitulo}</p>
      <p className="curso-card__desc">{curso.descricaoCurta}</p>
      <p className="curso-card__meta">{total} módulos</p>
      <ProgressBar percent={percent(total)} />
    </Link>
  )
}
```
```css
.curso-card { display: block; background: var(--branco); border: 1px solid var(--cinza-200); border-radius: var(--raio); padding: 1.5rem; box-shadow: var(--sombra); color: inherit; transition: transform .15s ease, box-shadow .15s ease; }
.curso-card:hover { transform: translateY(-2px); box-shadow: 0 6px 16px rgba(15,23,42,.12); text-decoration: none; }
.curso-card__icone { font-size: 2rem; }
.curso-card__titulo { margin: .5rem 0 .25rem; }
.curso-card__subtitulo { margin: 0; color: var(--azul-700); font-weight: 600; }
.curso-card__desc { color: var(--cinza-700); margin: .5rem 0; }
.curso-card__meta { color: var(--cinza-500); font-size: .85rem; margin: .5rem 0; }
```

- [ ] **Step 4: `Header.jsx` + `Header.css`**

```jsx
import { Link } from 'react-router-dom'
import './Header.css'

export function Header() {
  return (
    <header className="cabecalho">
      <div className="cabecalho__interno">
        <Link to="/" className="cabecalho__marca">▦ Portal de Treinamentos</Link>
      </div>
    </header>
  )
}
```
```css
.cabecalho { background: var(--azul-900); color: var(--branco); }
.cabecalho__interno { max-width: var(--max-largura); margin: 0 auto; padding: 1rem; }
.cabecalho__marca { color: var(--branco); font-weight: 700; font-size: 1.1rem; }
.cabecalho__marca:hover { text-decoration: none; opacity: .9; }
```

- [ ] **Step 5: `Layout.jsx` + `Layout.css`**

```jsx
import { Outlet } from 'react-router-dom'
import { Header } from './Header.jsx'

export function Layout() {
  return (
    <>
      <Header />
      <main className="container">
        <Outlet />
      </main>
    </>
  )
}
```
```css
/* Layout.css reservado para ajustes futuros do main; container já em index.css */
```

> Opcional: o Header e o CourseCard podem ser refinados depois com o Magic MCP mantendo as mesmas props/classe. Não bloqueia o plano.

- [ ] **Step 6: Verificar build**

Run: `npm run build`
Expected: build conclui sem erro.

- [ ] **Step 7: Commit**

```bash
git add -A && git commit -m "feat(components): ProgressBar, SearchBox, CourseCard, Header e Layout"
```

---

## Task 8: ModuleList e ModuleReader

**Files:**
- Create: `src/components/ModuleList.jsx` + `ModuleList.css`
- Create: `src/components/ModuleReader.jsx` + `ModuleReader.css`

- [ ] **Step 1: `ModuleList.jsx` + `ModuleList.css`**

```jsx
import { Link } from 'react-router-dom'
import './ModuleList.css'

export function ModuleList({ cursoId, modulos, isDone }) {
  return (
    <ol className="mod-lista">
      {modulos.map((m) => (
        <li key={m.id} className="mod-lista__item">
          <Link to={`/curso/${cursoId}/${m.id}`} className="mod-lista__link">
            <span className={`mod-lista__check ${isDone(m.id) ? 'is-done' : ''}`} aria-hidden="true">
              {isDone(m.id) ? '✓' : m.numero}
            </span>
            <span className="mod-lista__texto">
              <strong>{m.titulo}</strong>
              {m.resumo && <span className="mod-lista__resumo">{m.resumo}</span>}
            </span>
          </Link>
        </li>
      ))}
    </ol>
  )
}
```
```css
.mod-lista { list-style: none; margin: 1rem 0; padding: 0; display: grid; gap: .5rem; }
.mod-lista__link { display: flex; gap: .75rem; align-items: flex-start; background: var(--branco); border: 1px solid var(--cinza-200); border-radius: var(--raio); padding: .9rem 1rem; box-shadow: var(--sombra); color: inherit; }
.mod-lista__link:hover { text-decoration: none; border-color: var(--azul-500); }
.mod-lista__check { flex: none; width: 1.75rem; height: 1.75rem; border-radius: 999px; background: var(--cinza-100); color: var(--cinza-700); display: grid; place-items: center; font-weight: 700; }
.mod-lista__check.is-done { background: var(--novidade-borda); color: #fff; }
.mod-lista__texto { display: flex; flex-direction: column; }
.mod-lista__resumo { color: var(--cinza-500); font-size: .9rem; }
```

- [ ] **Step 2: `ModuleReader.jsx` + `ModuleReader.css`**

```jsx
import { Link } from 'react-router-dom'
import { BlockRenderer } from './blocks/BlockRenderer.jsx'
import './ModuleReader.css'

export function ModuleReader({ cursoId, modulo, done, onToggle, anterior, proximo }) {
  return (
    <article className="leitor">
      <p className="leitor__eyebrow">Módulo {modulo.numero}</p>
      <h1 className="leitor__titulo">{modulo.titulo}</h1>

      <div className="leitor__conteudo">
        {modulo.blocos.map((b, i) => <BlockRenderer key={i} bloco={b} />)}
      </div>

      <div className="leitor__acoes">
        <button
          type="button"
          className={`btn-concluir ${done ? 'is-done' : ''}`}
          onClick={onToggle}
        >
          {done ? '✓ Módulo concluído' : 'Marcar como concluído'}
        </button>
      </div>

      <nav className="leitor__nav">
        {anterior
          ? <Link to={`/curso/${cursoId}/${anterior.id}`}>← {anterior.titulo}</Link>
          : <span />}
        {proximo
          ? <Link to={`/curso/${cursoId}/${proximo.id}`}>{proximo.titulo} →</Link>
          : <span />}
      </nav>
    </article>
  )
}
```
```css
.leitor__eyebrow { color: var(--cinza-500); text-transform: uppercase; letter-spacing: .05em; font-size: .8rem; margin: 0; }
.leitor__titulo { margin: .25rem 0 1rem; }
.leitor__acoes { margin: 2rem 0 1rem; }
.btn-concluir { background: var(--azul-500); color: #fff; border: none; border-radius: var(--raio); padding: .7rem 1.25rem; font-size: 1rem; cursor: pointer; }
.btn-concluir:hover { background: var(--azul-700); }
.btn-concluir.is-done { background: var(--novidade-borda); }
.leitor__nav { display: flex; justify-content: space-between; gap: 1rem; margin-top: 2rem; border-top: 1px solid var(--cinza-200); padding-top: 1rem; }
```

- [ ] **Step 3: Verificar build**

Run: `npm run build`
Expected: build conclui sem erro.

- [ ] **Step 4: Commit**

```bash
git add -A && git commit -m "feat(components): ModuleList e ModuleReader"
```

---

## Task 9: Páginas e roteamento

**Files:**
- Create: `src/pages/HomePage.jsx` + `HomePage.css`
- Create: `src/pages/CoursePage.jsx` + `CoursePage.css`
- Create: `src/pages/ModulePage.jsx` + `ModulePage.css`
- Modify: `src/App.jsx` (substituir template)
- Modify: `src/main.jsx` (envolver com BrowserRouter)

- [ ] **Step 1: `HomePage.jsx` + `HomePage.css`**

```jsx
import { useState } from 'react'
import { Link } from 'react-router-dom'
import { getCourses } from '../data/courses/index.js'
import { searchModules } from '../lib/search.js'
import { CourseCard } from '../components/CourseCard.jsx'
import { SearchBox } from '../components/SearchBox.jsx'
import './HomePage.css'

export function HomePage() {
  const [q, setQ] = useState('')
  const cursos = getCourses()
  const resultados = searchModules(q)

  return (
    <>
      <h1 className="home__titulo">Treinamentos</h1>
      <p className="home__sub">Escolha um treinamento ou busque um tópico.</p>
      <SearchBox valor={q} onChange={setQ} />

      {q.trim() ? (
        <section className="home__resultados">
          <h2>{resultados.length} resultado(s)</h2>
          <ul className="home__lista-result">
            {resultados.map(({ curso, modulo }) => (
              <li key={`${curso.id}/${modulo.id}`}>
                <Link to={`/curso/${curso.id}/${modulo.id}`}>
                  <strong>{modulo.titulo}</strong> — {curso.titulo}
                </Link>
              </li>
            ))}
          </ul>
        </section>
      ) : (
        <section className="home__grade">
          {cursos.map((c) => <CourseCard key={c.id} curso={c} />)}
        </section>
      )}
    </>
  )
}
```
```css
.home__titulo { margin-bottom: .25rem; }
.home__sub { color: var(--cinza-500); margin-top: 0; }
.home__grade { display: grid; gap: 1.25rem; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); margin-top: 1.5rem; }
.home__resultados { margin-top: 1.5rem; }
.home__lista-result { list-style: none; padding: 0; display: grid; gap: .5rem; }
.home__lista-result a { display: block; background: var(--branco); border: 1px solid var(--cinza-200); border-radius: var(--raio); padding: .8rem 1rem; }
```

- [ ] **Step 2: `CoursePage.jsx` + `CoursePage.css`**

```jsx
import { useParams, Link, Navigate } from 'react-router-dom'
import { getCourse } from '../data/courses/index.js'
import { useProgress } from '../hooks/useProgress.js'
import { ProgressBar } from '../components/ProgressBar.jsx'
import { ModuleList } from '../components/ModuleList.jsx'
import './CoursePage.css'

export function CoursePage() {
  const { cursoId } = useParams()
  const curso = getCourse(cursoId)
  const { isDone, percent, completedCount } = useProgress(cursoId)
  if (!curso) return <Navigate to="/" replace />

  const total = curso.modulos.length
  return (
    <>
      <p className="curso__voltar"><Link to="/">← Todos os treinamentos</Link></p>
      <h1>{curso.titulo}</h1>
      <p className="curso__sub">{curso.subtitulo}</p>
      <div className="curso__progresso">
        <ProgressBar percent={percent(total)} label={`${completedCount}/${total} concluídos`} />
      </div>
      <ModuleList cursoId={curso.id} modulos={curso.modulos} isDone={isDone} />
    </>
  )
}
```
```css
.curso__voltar { margin: 0 0 .5rem; }
.curso__sub { color: var(--azul-700); font-weight: 600; margin-top: 0; }
.curso__progresso { max-width: 360px; margin: 1rem 0; }
```

- [ ] **Step 3: `ModulePage.jsx` + `ModulePage.css`**

```jsx
import { useParams, Link, Navigate } from 'react-router-dom'
import { getCourse, getModule } from '../data/courses/index.js'
import { useProgress } from '../hooks/useProgress.js'
import { ModuleReader } from '../components/ModuleReader.jsx'
import './ModulePage.css'

export function ModulePage() {
  const { cursoId, moduloId } = useParams()
  const curso = getCourse(cursoId)
  const modulo = getModule(cursoId, moduloId)
  const { isDone, toggle } = useProgress(cursoId)
  if (!curso || !modulo) return <Navigate to="/" replace />

  const idx = curso.modulos.findIndex((m) => m.id === moduloId)
  const anterior = curso.modulos[idx - 1]
  const proximo = curso.modulos[idx + 1]

  return (
    <>
      <p className="modulo__voltar"><Link to={`/curso/${cursoId}`}>← {curso.titulo}</Link></p>
      <ModuleReader
        cursoId={cursoId}
        modulo={modulo}
        done={isDone(moduloId)}
        onToggle={() => toggle(moduloId)}
        anterior={anterior}
        proximo={proximo}
      />
    </>
  )
}
```
```css
.modulo__voltar { margin: 0 0 .5rem; }
```

- [ ] **Step 4: Substituir `src/App.jsx`**

```jsx
import { Routes, Route, Navigate } from 'react-router-dom'
import { Layout } from './components/Layout.jsx'
import { HomePage } from './pages/HomePage.jsx'
import { CoursePage } from './pages/CoursePage.jsx'
import { ModulePage } from './pages/ModulePage.jsx'

export default function App() {
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route path="/" element={<HomePage />} />
        <Route path="/curso/:cursoId" element={<CoursePage />} />
        <Route path="/curso/:cursoId/:moduloId" element={<ModulePage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  )
}
```

- [ ] **Step 5: Substituir `src/main.jsx`**

```jsx
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter } from 'react-router-dom'
import App from './App.jsx'
import './index.css'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <BrowserRouter>
      <App />
    </BrowserRouter>
  </StrictMode>,
)
```

- [ ] **Step 6: Remover restos do template**

Run:
```bash
rm -f src/App.css src/assets/hero.png src/assets/react.svg src/assets/vite.svg
```
(Se algum import remanescente quebrar o build, remover o import correspondente.)

- [ ] **Step 7: Verificar build e lint**

Run: `npm run build && npm run lint`
Expected: build gera `dist/` sem erro; lint sem erros.

- [ ] **Step 8: Commit**

```bash
git add -A && git commit -m "feat(pages): Home, Curso e Módulo com roteamento completo"
```

---

## Task 10: Deploy Vercel e verificação final

**Files:**
- Create: `vercel.json`
- Modify: `README.md`

- [ ] **Step 1: Criar `vercel.json` (rewrite SPA)**

```json
{
  "rewrites": [{ "source": "/(.*)", "destination": "/index.html" }]
}
```

- [ ] **Step 2: Reescrever `README.md`**

```markdown
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
```

- [ ] **Step 3: Rodar a suíte completa**

Run: `npm test`
Expected: PASS em todos os arquivos (courses, useProgress, search, BlockRenderer).

- [ ] **Step 4: Verificação manual no dev server**

Run: `npm run dev` e abrir o navegador. Conferir:
- Home mostra 2 cards com 0% de progresso.
- Buscar "estanqueidade" / "óleo" retorna módulos.
- Abrir um módulo: tabelas e callouts renderizam; "Marcar como concluído" alterna e persiste após recarregar (F5).
- Voltar à Home: barra de progresso do curso atualizada.
- Deep link direto (ex.: recarregar em `/curso/postos/modulo-2`) funciona no dev.

- [ ] **Step 5: Commit final**

```bash
git add -A && git commit -m "chore: config de deploy Vercel e README"
```

---

## Self-Review (preenchido)

**Spec coverage:**
- Modelo de conteúdo estruturado → Tasks 1–2. ✓
- Portal único + cursos → Task 9 (HomePage) + Task 7 (CourseCard). ✓
- Rotas `/`, `/curso/:id`, `/curso/:id/:mod` + fallback → Task 9. ✓
- Progresso em localStorage + barra/✓ → Task 3 + Tasks 7–9. ✓
- Busca client-side → Task 4 + HomePage. ✓
- Renderização de tabelas e callouts (⚠/ℹ/★) e pontos-chave → Task 6. ✓
- Visual corporativo limpo (tokens CSS) → Task 5 + CSS por componente. ✓
- Deploy Vercel (rewrite SPA) → Task 10. ✓
- Limpeza do template → Task 9 Step 6 + Task 0. ✓
- Acentuação de Fluidos restaurada → Task 2 Step 3. ✓
- Critérios de sucesso (build/lint/persistência/deep link) → Task 9 Step 7 + Task 10 Steps 3–4. ✓

**Placeholder scan:** Sem "TODO/TBD" em código. A Task 2 é transcrição de conteúdo (dado), não lógica — define padrão completo com 1 módulo totalmente mapeado e o procedimento de extração; aceitável por ser autoria de dados a partir da fonte (`.docx`).

**Type consistency:** Props/funções conferem entre tasks — `useProgress` expõe `isDone/toggle/percent/completedCount` (Task 3) e é consumido com essas mesmas chaves nas Tasks 7–9; `getCourses/getCourse/getModule` (Task 1) usados consistentemente; blocos seguem os tipos do esquema (Task 1) em render (Task 6) e busca (Task 4).
