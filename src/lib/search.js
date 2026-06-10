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
