import './DataTable.css'

export function DataTable({ colunas, linhas }) {
  return (
    <div className="tabela-wrap">
      <table className="tabela">
        <thead>
          <tr>{colunas.map((c, i) => <th key={i}>{c}</th>)}</tr>
        </thead>
        <tbody>
          {linhas.map((linha, r) => (
            <tr key={r}>{linha.map((cel, c) => <td key={c}>{cel}</td>)}</tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}
