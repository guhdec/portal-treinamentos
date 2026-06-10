import './ProgressBar.css'

export function ProgressBar({ percent, label }) {
  return (
    <div className="progresso">
      <div className="progresso__trilho">
        <div className="progresso__barra" style={{ width: `${percent}%` }} />
      </div>
      <span className="progresso__rotulo">{label ?? `${percent}%`}</span>
    </div>
  )
}
