export function BulletList({ itens }) {
  return (
    <ul className="bloco-lista">
      {itens.map((it, i) => <li key={i}>{it}</li>)}
    </ul>
  )
}
