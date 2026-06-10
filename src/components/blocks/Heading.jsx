export function Heading({ nivel = 3, texto }) {
  const Tag = nivel === 2 ? 'h2' : 'h3'
  return <Tag className="bloco-titulo">{texto}</Tag>
}
