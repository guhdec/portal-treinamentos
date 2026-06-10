# Esquema de dados de cursos

Curso  = { id, titulo, subtitulo, descricaoCurta, icone, capa?, modulos: [Modulo] }
Modulo = { id, numero, titulo, resumo, blocos: [Bloco] }

Bloco (campo `tipo` discrimina):
- { tipo: "titulo", nivel: 2|3, texto }
- { tipo: "paragrafo", texto }
- { tipo: "lista", itens: [string] }
- { tipo: "tabela", colunas: [string], linhas: [[string]] }
- { tipo: "callout", variante: "alerta"|"info"|"novidade", titulo?, texto?, itens?: [string] }
- { tipo: "pontos-chave", itens: [string] }   // "O QUE O GERENTE PRECISA SABER"
- { tipo: "imagem", src, alt?, legenda?, largura?: "larga" }   // src = caminho em /public

Regras:
- id de curso e de módulo são kebab-case, únicos.
- módulos usam id "modulo-N" (N = numero).
- `icone`: string curta (emoji) usada nos cards.
- `capa`: caminho de imagem (ex.: "/img/posto-render-2.jpg") usada como capa no card e hero do curso.
