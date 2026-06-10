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
