import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { BlockRenderer } from './BlockRenderer.jsx'

describe('BlockRenderer', () => {
  it('renderiza parágrafo', () => {
    render(<BlockRenderer bloco={{ tipo: 'paragrafo', texto: 'Olá mundo' }} />)
    expect(screen.getByText('Olá mundo')).toBeInTheDocument()
  })
  it('renderiza tabela com cabeçalhos e células', () => {
    render(<BlockRenderer bloco={{ tipo: 'tabela', colunas: ['A', 'B'], linhas: [['1', '2']] }} />)
    expect(screen.getByText('A')).toBeInTheDocument()
    expect(screen.getByText('2')).toBeInTheDocument()
  })
  it('renderiza callout com título', () => {
    render(<BlockRenderer bloco={{ tipo: 'callout', variante: 'alerta', titulo: 'Atenção', texto: 'cuidado' }} />)
    expect(screen.getByText('Atenção')).toBeInTheDocument()
    expect(screen.getByText('cuidado')).toBeInTheDocument()
  })
  it('renderiza pontos-chave', () => {
    render(<BlockRenderer bloco={{ tipo: 'pontos-chave', itens: ['ponto um'] }} />)
    expect(screen.getByText('ponto um')).toBeInTheDocument()
  })
})
