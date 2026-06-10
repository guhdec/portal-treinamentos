import { describe, it, expect } from 'vitest'
import { getCourses, getCourse, getModule } from '../data/courses/index.js'

const TIPOS = new Set(['titulo', 'paragrafo', 'lista', 'tabela', 'callout', 'pontos-chave', 'imagem'])

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
