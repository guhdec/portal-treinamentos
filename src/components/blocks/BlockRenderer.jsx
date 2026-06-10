import './blocks.css'
import { Heading } from './Heading.jsx'
import { Paragraph } from './Paragraph.jsx'
import { BulletList } from './BulletList.jsx'
import { Callout } from './Callout.jsx'
import { DataTable } from './DataTable.jsx'
import { KeyPoints } from './KeyPoints.jsx'

export function BlockRenderer({ bloco }) {
  switch (bloco.tipo) {
    case 'titulo':       return <Heading nivel={bloco.nivel} texto={bloco.texto} />
    case 'paragrafo':    return <Paragraph texto={bloco.texto} />
    case 'lista':        return <BulletList itens={bloco.itens} />
    case 'tabela':       return <DataTable colunas={bloco.colunas} linhas={bloco.linhas} />
    case 'callout':      return <Callout {...bloco} />
    case 'pontos-chave': return <KeyPoints itens={bloco.itens} />
    default:             return null
  }
}
