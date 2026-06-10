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
