import './Callout.css'

const ICONE = { alerta: '⚠', info: 'ℹ', novidade: '★' }

export function Callout({ variante = 'info', titulo, texto, itens }) {
  return (
    <div className={`callout callout--${variante}`} role="note">
      <div className="callout__cabecalho">
        <span className="callout__icone" aria-hidden="true">{ICONE[variante]}</span>
        {titulo && <strong className="callout__titulo">{titulo}</strong>}
      </div>
      {texto && <p className="callout__texto">{texto}</p>}
      {itens && (
        <ul className="callout__lista">
          {itens.map((it, i) => <li key={i}>{it}</li>)}
        </ul>
      )}
    </div>
  )
}
