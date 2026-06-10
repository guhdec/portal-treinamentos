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
      {curso.capa && (
        <div className="curso__hero">
          <img src={curso.capa} alt="" />
        </div>
      )}
      <h1 className="curso__titulo">{curso.titulo}</h1>
      <p className="curso__sub">{curso.subtitulo}</p>
      <div className="curso__progresso">
        <ProgressBar percent={percent(total)} label={`${completedCount}/${total} concluídos`} />
      </div>
      <ModuleList cursoId={curso.id} modulos={curso.modulos} isDone={isDone} />
    </>
  )
}
