import { Link } from 'react-router-dom'
import { ProgressBar } from './ProgressBar.jsx'
import { useProgress } from '../hooks/useProgress.js'
import './CourseCard.css'

export function CourseCard({ curso }) {
  const { percent } = useProgress(curso.id)
  const total = curso.modulos.length
  return (
    <Link to={`/curso/${curso.id}`} className="curso-card">
      {curso.capa && (
        <div className="curso-card__capa">
          <img src={curso.capa} alt="" loading="lazy" />
          {curso.icone && <span className="curso-card__icone" aria-hidden="true">{curso.icone}</span>}
        </div>
      )}
      <div className="curso-card__corpo">
        <h2 className="curso-card__titulo">{curso.titulo}</h2>
        <p className="curso-card__subtitulo">{curso.subtitulo}</p>
        <p className="curso-card__desc">{curso.descricaoCurta}</p>
        <p className="curso-card__meta">{total} módulos</p>
        <ProgressBar percent={percent(total)} />
      </div>
    </Link>
  )
}
