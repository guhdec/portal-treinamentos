import { Link } from 'react-router-dom'
import './Header.css'

export function Header() {
  return (
    <header className="cabecalho">
      <div className="cabecalho__interno">
        <Link to="/" className="cabecalho__marca">▦ Portal de Treinamentos</Link>
      </div>
    </header>
  )
}
