import './KeyPoints.css'

export function KeyPoints({ itens }) {
  return (
    <div className="pontos-chave">
      <h3 className="pontos-chave__titulo">★ O que você precisa saber</h3>
      <ol className="pontos-chave__lista">
        {itens.map((it, i) => <li key={i}>{it}</li>)}
      </ol>
    </div>
  )
}
