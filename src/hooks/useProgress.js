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
