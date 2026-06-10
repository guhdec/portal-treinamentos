import './Figure.css'

export function Figure({ src, alt = '', legenda, largura }) {
  return (
    <figure className={`figura ${largura === 'larga' ? 'figura--larga' : ''}`}>
      <img className="figura__img" src={src} alt={alt} loading="lazy" />
      {legenda && <figcaption className="figura__legenda">{legenda}</figcaption>}
    </figure>
  )
}
