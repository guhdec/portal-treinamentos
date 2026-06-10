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
