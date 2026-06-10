import { Link } from 'react-router-dom'
import { BlockRenderer } from './blocks/BlockRenderer.jsx'
import './ModuleReader.css'

export function ModuleReader({ cursoId, modulo, done, onToggle, anterior, proximo }) {
  return (
    <article className="leitor">
      <p className="leitor__eyebrow">Módulo {modulo.numero}</p>
      <h1 className="leitor__titulo">{modulo.titulo}</h1>

      <div className="leitor__conteudo">
        {modulo.blocos.map((b, i) => <BlockRenderer key={i} bloco={b} />)}
      </div>

      <div className="leitor__acoes">
        <button
          type="button"
          className={`btn-concluir ${done ? 'is-done' : ''}`}
          onClick={onToggle}
        >
          {done ? '✓ Módulo concluído' : 'Marcar como concluído'}
        </button>
      </div>

      <nav className="leitor__nav">
        {anterior
          ? <Link to={`/curso/${cursoId}/${anterior.id}`}>← {anterior.titulo}</Link>
          : <span />}
        {proximo
          ? <Link to={`/curso/${cursoId}/${proximo.id}`}>{proximo.titulo} →</Link>
          : <span />}
      </nav>
    </article>
  )
}
