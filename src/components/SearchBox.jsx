import './SearchBox.css'

export function SearchBox({ valor, onChange, placeholder = 'Buscar nos treinamentos…' }) {
  return (
    <input
      type="search"
      className="busca"
      value={valor}
      onChange={(e) => onChange(e.target.value)}
      placeholder={placeholder}
      aria-label="Buscar"
    />
  )
}
