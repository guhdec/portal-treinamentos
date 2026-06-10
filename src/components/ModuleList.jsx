import { Link } from 'react-router-dom'
import './ModuleList.css'

export function ModuleList({ cursoId, modulos, isDone }) {
  return (
    <ol className="mod-lista">
      {modulos.map((m) => (
        <li key={m.id} className="mod-lista__item">
          <Link to={`/curso/${cursoId}/${m.id}`} className="mod-lista__link">
            <span className={`mod-lista__check ${isDone(m.id) ? 'is-done' : ''}`} aria-hidden="true">
              {isDone(m.id) ? '✓' : m.numero}
            </span>
            <span className="mod-lista__texto">
              <strong>{m.titulo}</strong>
              {m.resumo && <span className="mod-lista__resumo">{m.resumo}</span>}
            </span>
          </Link>
        </li>
      ))}
    </ol>
  )
}
