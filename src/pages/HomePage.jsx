import { useState } from 'react'
import { Link } from 'react-router-dom'
import { getCourses } from '../data/courses/index.js'
import { searchModules } from '../lib/search.js'
import { CourseCard } from '../components/CourseCard.jsx'
import { SearchBox } from '../components/SearchBox.jsx'
import './HomePage.css'

export function HomePage() {
  const [q, setQ] = useState('')
  const cursos = getCourses()
  const resultados = searchModules(q)

  return (
    <>
      <h1 className="home__titulo">Treinamentos</h1>
      <p className="home__sub">Escolha um treinamento ou busque um tópico.</p>
      <SearchBox valor={q} onChange={setQ} />

      {q.trim() ? (
        <section className="home__resultados">
          <h2>{resultados.length} resultado(s)</h2>
          <ul className="home__lista-result">
            {resultados.map(({ curso, modulo }) => (
              <li key={`${curso.id}/${modulo.id}`}>
                <Link to={`/curso/${curso.id}/${modulo.id}`}>
                  <strong>{modulo.titulo}</strong> — {curso.titulo}
                </Link>
              </li>
            ))}
          </ul>
        </section>
      ) : (
        <section className="home__grade">
          {cursos.map((c) => <CourseCard key={c.id} curso={c} />)}
        </section>
      )}
    </>
  )
}
