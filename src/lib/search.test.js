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
