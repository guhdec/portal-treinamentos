import { Link } from 'react-router-dom'
import './Header.css'

export function Header() {
  return (
    <header className="cabecalho">
      <div className="cabecalho__interno">
        <Link to="/" className="cabecalho__marca" aria-label="Audax — início">
          <img src="/img/logo-audax-h-white.png" alt="Audax" className="cabecalho__logo" />
          <span className="cabecalho__divisor" aria-hidden="true" />
          <span className="cabecalho__txt">Treinamentos</span>
        </Link>
      </div>
    </header>
  )
}
