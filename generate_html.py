#!/usr/bin/env python3
"""Generate training HTML from extracted docx content."""
import json
import re
import html

BASE = r"c:\TREINAMENTO HTML"

def esc(text):
    return html.escape(text)

def render_table(headers, rows):
    h = "<table><thead><tr>" + "".join(f"<th>{esc(c)}</th>" for c in headers) + "</tr></thead><tbody>"
    for row in rows:
        h += "<tr>" + "".join(f"<td>{esc(c)}</td>" for c in row) + "</tr>"
    return h + "</tbody></table>"

def wrap_list(items, ordered=False):
    tag = "ol" if ordered else "ul"
    inner = "".join(f"<li>{esc(i)}</li>" for i in items)
    return f"<{tag}>{inner}</{tag}>"

def callout(text, kind="info"):
    cls = {"★": "highlight", "⚠": "warning", "ℹ": "info", "✔": "tip"}.get(text[0], "info")
    return f'<div class="callout {cls}">{esc(text)}</div>'

# --- Pre-built tables (from docx structure) ---
FLUIDOS_DOT_TABLE = {
    "headers": ["Característica", "DOT 3", "DOT 4"],
    "rows": [
        ["Base química", "Glicol éter", "Glicol éter com borato"],
        ["Ebulicação — fluido seco", "Mínimo 205 graus C", "Mínimo 230 graus C"],
        ["Ebulicação — fluido úmido", "Mínimo 140 graus C", "Mínimo 155 graus C"],
        ["Uso típico", "Veículos mais antigos, freios a disco e tambor simples", "Veículos modernos com ABS, ESP e frenagem regenerativa"],
        ["Intervalo de troca recomendado", "A cada 1 ano ou 20.000 km", "A cada 1 a 2 anos ou 30.000 km"],
    ],
}

FLUIDOS_OIL_TABLE = {
    "headers": ["Óleo", "Frio (partida)", "Calor (operação)", "Clima indicado", "Uso típico"],
    "rows": [
        ["0W-20", "Muito fluido", "Fino", "Frio e temperado", "Veículos flex e híbridos modernos, máximo de eficiência"],
        ["5W-30", "Fluido", "Médio", "Temperado a quente", "Maioria dos veículos flex modernos: HB20, Onix, Argo e similares"],
        ["15W-40", "Menos fluido", "Grosso", "Clima quente", "Motores a diesel, caminhões e frotas em geral"],
        ["20W-50", "Espesso", "Muito grosso", "Clima muito quente", "Motores antigos com desgaste elevado e maior quilometragem"],
    ],
}

FLUIDOS_SITUACOES_TABLE = {
    "headers": ["Situação", "Como orientar"],
    "rows": [
        ["Onix, HB20, Argo (pós-2015)", "Quase sempre 5W-30 sintético. Confirmar sempre no manual do veículo."],
        ["Corolla ou Civic automático", "Requer ATF — confirmar o tipo exato exigido pelo fabricante (Toyota T-IV, Honda DW-1, etc.)."],
        ["Caminhão ou van (ex.: Sprinter)", "Geralmente 15W-40 diesel. Verificar classificação API adequada (CJ-4 ou equivalente)."],
        ["Veículo antigo com motor barulhento", "Pode indicar 20W-50 mineral. Orientar o cliente a consultar um mecânico também."],
        ["Cliente pede fluido de freio sem saber o tipo", "Verifique a tampa do reservatório de freio do veículo — o tipo estará gravado nela (DOT 3 ou DOT 4)."],
    ],
}

FLUIDOS_RESUMO_TABLE = {
    "headers": ["Produto", "Para que serve", "Onde confirmar", "Ponto de atenção"],
    "rows": [
        ["DOT 3", "Fluido de freio hidráulico", "Tampa do reservatório de freio", "Ponto de ebulição mais baixo. Indicado para veículos mais antigos."],
        ["DOT 4", "Fluido de freio hidráulico", "Tampa do reservatório de freio", "Exigido em veículos com ABS ou ESP. Maior resistência ao calor."],
        ["ATF", "Câmbio automático e direção hidráulica", "Manual do veículo — especificação própria por marca", "Tipos não são intercambiáveis. Confirmar sempre antes de vender."],
        ["0W-20", "Óleo de motor", "Manual do veículo", "Veículos modernos e híbridos. Máximo de eficiência e economia."],
        ["5W-30", "Óleo de motor", "Manual do veículo", "Uso geral em veículos flex modernos. O mais solicitado no dia a dia."],
        ["15W-40", "Óleo de motor", "Manual do veículo", "Indicado para diesel, caminhões e frotas."],
        ["20W-50", "Óleo de motor", "Manual do veículo", "Para motores antigos com maior desgaste e quilometragem elevada."],
    ],
}

SKIP_MARKERS = {
    "Caracteristica", "DOT 3", "DOT 4", "Base quimica", "Glicol eter", "Glicol eter com borato",
    "Ebulicao — fluido seco", "Minimo 205 graus C", "Minimo 230 graus C",
    "Ebulicao — fluido umido", "Minimo 140 graus C", "Minimo 155 graus C",
    "Uso tipico", "Veiculos mais antigos, freios a disco e tambor simples",
    "Veiculos modernos com ABS, ESP e frenagem regenerativa",
    "Intervalo de troca recomendado", "A cada 1 ano ou 20.000 km", "A cada 1 a 2 anos ou 30.000 km",
    "Oleo", "Frio (partida)", "Calor (operacao)", "Clima indicado", "Uso tipico",
    "0W-20", "Muito fluido", "Fino", "Frio e temperado",
    "Veiculos flex e hibridos modernos, maximo de eficiencia",
    "5W-30", "Fluido", "Medio", "Temperado a quente",
    "Maioria dos veiculos flex modernos: HB20, Onix, Argo e similares",
    "15W-40", "Menos fluido", "Grosso", "Clima quente",
    "Motores a diesel, caminhoes e frotas em geral",
    "20W-50", "Espesso", "Muito grosso", "Clima muito quente",
    "Motores antigos com desgaste elevado e maior quilometragem",
    "Situacao", "Como orientar",
    "Onix, HB20, Argo (pos-2015)", "Quase sempre 5W-30 sintetico. Confirmar sempre no manual do veiculo.",
    "Corolla ou Civic automatico", "Requer ATF — confirmar o tipo exato exigido pelo fabricante (Toyota T-IV, Honda DW-1, etc.).",
    "Caminhao ou van (ex.: Sprinter)", "Geralmente 15W-40 diesel. Verificar classificacao API adequada (CJ-4 ou equivalente).",
    "Veiculo antigo com motor barulhento", "Pode indicar 20W-50 mineral. Orientar o cliente a consultar um mecanico tambem.",
    "Cliente pede fluido de freio sem saber o tipo",
    "Verifique a tampa do reservatorio de freio do veiculo — o tipo estara gravado nela (DOT 3 ou DOT 4).",
    "Produto", "Para que serve", "Onde confirmar o tipo correto", "Ponto de atencao",
    "Fluido de freio hidraulico", "Tampa do reservatorio de freio",
    "Ponto de ebulicao mais baixo. Indicado para veiculos mais antigos.",
    "Exigido em veiculos com ABS ou ESP. Maior resistencia ao calor.",
    "Cambio automatico e direcao hidraulica", "Manual do veiculo — especificacao propria por marca",
    "Tipos nao sao intercambiaveis. Confirmar sempre antes de vender.",
    "Oleo de motor", "Manual do veiculo",
    "Veiculos modernos e hibridos. Maximo de eficiencia e economia.",
    "Uso geral em veiculos flex modernos. O mais solicitado no dia a dia.",
    "Indicado para diesel, caminhoes e frotas.",
    "Para motores antigos com maior desgaste e quilometragem elevada.",
    "TREINAMENTO", "Fluidos Automotivos", "Para Frentistas e Gerentes",
    "Produtos: DOT 3  |  DOT 4  |  ATF  |  5W-30  |  0W-20  |  15W-40  |  20W-50",
}

def render_fluidos(paragraphs):
    parts = []
    i = 0
    section_open = False
    list_open = False

    def close_list():
        nonlocal list_open
        if list_open:
            parts.append("</ul>")
            list_open = False

    def close_section():
        nonlocal section_open
        close_list()
        if section_open:
            parts.append("</section>")
            section_open = False

    def open_list():
        nonlocal list_open
        if not list_open:
            parts.append("<ul>")
            list_open = True

    def skip_table_data(idx):
        while idx < len(paragraphs) and paragraphs[idx] in SKIP_MARKERS:
            idx += 1
        return idx

    while i < len(paragraphs):
        p = paragraphs[i]
        if p in ("TREINAMENTO", "Fluidos Automotivos", "Para Frentistas e Gerentes",
                 "Produtos: DOT 3  |  DOT 4  |  ATF  |  5W-30  |  0W-20  |  15W-40  |  20W-50"):
            i += 1
            continue
        if p in SKIP_MARKERS:
            i += 1
            continue

        if p == "Regra de Ouro":
            close_section()
            parts.append(f'<div class="golden-rule"><h3>{esc(p)}</h3><p>{esc(paragraphs[i+1])}</p></div>')
            i += 2
            continue

        if re.match(r"^Modulo \d", p, re.I):
            close_section()
            parts.append(f'<section class="module"><h2>{esc(p)}</h2>')
            section_open = True
            i += 1
            continue

        if p == "Resumo para Consulta Rapida":
            close_section()
            parts.append(f'<section class="module summary-module"><h2>{esc(p)}</h2>')
            parts.append(f'<p>{esc(paragraphs[i+1])}</p>')
            parts.append(render_table(FLUIDOS_RESUMO_TABLE["headers"], FLUIDOS_RESUMO_TABLE["rows"]))
            parts.append(f'<p class="footer-note">{esc(paragraphs[-1])}</p></section>')
            break

        if p == "1.3 DOT 3 x DOT 4 — Comparativo":
            close_list()
            parts.append(f'<h3>{esc(p)}</h3>')
            parts.append(render_table(FLUIDOS_DOT_TABLE["headers"], FLUIDOS_DOT_TABLE["rows"]))
            i = skip_table_data(i + 1)
            continue

        if p == "3.2 Comparativo dos quatro oleos":
            close_list()
            parts.append(f'<h3>{esc(p)}</h3>')
            parts.append(render_table(FLUIDOS_OIL_TABLE["headers"], FLUIDOS_OIL_TABLE["rows"]))
            i = skip_table_data(i + 1)
            continue

        if p == "4.2 Situacoes comuns e como agir":
            close_list()
            parts.append(f'<h3>{esc(p)}</h3>')
            parts.append(render_table(FLUIDOS_SITUACOES_TABLE["headers"], FLUIDOS_SITUACOES_TABLE["rows"]))
            i = skip_table_data(i + 1)
            continue

        if re.match(r"^\d+\.\d+\s", p):
            close_list()
            parts.append(f'<h3>{esc(p)}</h3>')
            i += 1
            continue

        if p.startswith("Atencao") or p.startswith("Atenção"):
            close_list()
            parts.append(callout(p, "warning"))
            i += 1
            continue

        if ":" in p and len(p) < 90 and not p.endswith("?"):
            open_list()
            parts.append(f'<li>{esc(p)}</li>')
            i += 1
            continue

        close_list()
        parts.append(f'<p>{esc(p)}</p>')
        i += 1

    close_section()
    return "\n".join(parts)

def render_gerentes(paragraphs):
    """Render gerentes content using sequential walk with explicit table data."""
    parts = []

    # Hero
    parts.append(f'''<div class="hero-gerentes">
      <p class="eyebrow">{esc(paragraphs[0])}</p>
      <h2>{esc(paragraphs[1])}<br>{esc(paragraphs[2])}<br>{esc(paragraphs[3])}</h2>
      <p class="version">{esc(paragraphs[4])}</p>
    </div>''')

    parts.append(f'''<div class="objective-box">
      <h3>{esc(paragraphs[5])}</h3>
      <p>{esc(paragraphs[6])}</p>
      <p class="orgs">{esc(paragraphs[7])}</p>
    </div>''')

    parts.append('''<nav class="module-toc"><h3>Índice dos Módulos</h3><ol>
      <li><a href="#modulo-01-avcb">Módulo 1: AVCB – Corpo de Bombeiros</a></li>
      <li><a href="#modulo-02-licenca">Módulo 2: Licença de Operação – CETESB</a></li>
      <li><a href="#modulo-03-alvara">Módulo 3: Alvará de Funcionamento – Prefeitura</a></li>
      <li><a href="#modulo-04-cadastro">Módulo 4: Cadastro de Tanques e Bombas / IPEM</a></li>
      <li><a href="#modulo-05-estanqueidade">Módulo 5: Laudo de Estanqueidade</a></li>
      <li><a href="#modulo-06-anp">Módulo 6: Ficha ANP / Autorização de Funcionamento</a></li>
    </ol></nav>''')

    parts.append(f'''<div class="callout warning conduct-box">
      <h3>⚠ {esc(paragraphs[14].replace("⚠ ", ""))}</h3>
      <p>{esc(paragraphs[15])}</p>
    </div>''')

    modules = [
        (16, 66, "modulo-01-avcb"),
        (66, 125, "modulo-02-licenca"),
        (125, 159, "modulo-03-alvara"),
        (159, 205, "modulo-04-cadastro"),
        (205, 245, "modulo-05-estanqueidade"),
        (245, 313, "modulo-06-anp"),
    ]

    for start, end, anchor in modules:
        chunk = paragraphs[start:end]
        parts.append(f'<section class="module" id="{anchor}">')
        parts.append(f'<h2>{esc(chunk[0])}</h2>')
        parts.append(f'<p class="module-sub">{esc(chunk[1])}</p>')
        parts.append(render_gerentes_chunk(chunk[2:]))
        parts.append('</section>')

    # Executive summary
    parts.append(f'<section class="module executive-summary"><h2>{esc(paragraphs[313])}</h2><p>{esc(paragraphs[314])}</p>')
    parts.append(render_table(
        ["Documento", "Órgão", "Validade", "Renovação", "Ação se irregular"],
        [
            ["AVCB (Dec. 69.118/2024)", "CBPMESP", "1–5 anos", "Antes do venc.", "Eng. de segurança"],
            ["Licença de Operação", "CETESB", "4–10 anos", "120 dias antes", "Protocolar e-CETESB"],
            ["Alvará de Funcionamento", "Prefeitura", "Anual", "Antes do venc.", "Regularizar na SMUL"],
            ["Cadastro Tanques/Bombas", "SMUL / IPEM", "Por equip.", "A cada alteração", "Resp. técnico + SMUL"],
            ["Laudo de Estanqueidade", "Empresa INMETRO", "12 meses ⚠", "120 dias antes", "Contratar ensaio"],
            ["Ficha ANP / FAC", "ANP", "Contínua", "A cada alteração", "Atualizar SRD-PR"],
            ["Selos IPEM (bombas)", "IPEM-SP", "12 meses ⚠", "Verif. anual IPEM", "Manut. autorizada"],
            ["Drenagem diesel (968/2024)", "ANP", "Semanal/quinzenal", "Registro contínuo", "Iniciar registros"],
        ]
    ))
    parts.append('</section>')

    parts.append(f'<div class="golden-rule"><h3>{esc(paragraphs[360])}</h3>')
    parts.append(wrap_list(paragraphs[361:367], ordered=True))
    parts.append('</div>')
    parts.append(f'<p class="doc-footer">{esc(paragraphs[367])}<br>{esc(paragraphs[368])}</p>')

    return "\n".join(parts)

def render_gerentes_chunk(chunk):
    """Render a module's body paragraphs."""
    out = []
    i = 0
    while i < len(chunk):
        p = chunk[i]

        if p == "O que é?":
            out.append(f'<h3>{esc(p)}</h3><p>{esc(chunk[i+1])}</p>')
            i += 2
            continue

        if p in ("Base Legal", "Base Legal Vigente em 2026"):
            out.append(f'<h3>{esc(p)}</h3>')
            i += 1
            if i < len(chunk) and chunk[i] == "Norma":
                rows = []
                j = i + 2
                while j + 1 < len(chunk) and chunk[j] not in ("★", "ℹ", "⚠", "Documentos", "Modalidade", "★  O QUE O GERENTE PRECISA SABER", "O que é?", "Conduta", "Pré-requisitos", "Consequências", "Verificação", "Etapas", "Resultado", "Onde", "Como", "Fiscalização", "O que Deve"):
                    if chunk[j].startswith("★") or chunk[j].startswith("ℹ") or chunk[j].startswith("⚠"):
                        break
                    rows.append([chunk[j], chunk[j+1]])
                    j += 2
                out.append(render_table(["Norma", "O que regula"], rows))
                i = j
            continue

        if p == "★  O QUE O GERENTE PRECISA SABER":
            items = []
            i += 1
            while i < len(chunk) and re.match(r"^\d+\.", chunk[i]):
                items.append(chunk[i])
                i += 1
            out.append(f'<div class="key-points"><h4>O que o gerente precisa saber</h4>{wrap_list(items, ordered=True)}</div>')
            continue

        if p == "Modalidades para Postos em SP":
            i += 1
            continue

        if p.startswith(("★", "⚠", "ℹ", "✔")):
            body = ""
            if i + 1 < len(chunk) and not chunk[i+1].startswith(("★", "⚠", "ℹ", "✔", "1.", "2.", "3.", "4.", "5.", "6.", "MÓDULO", "O que", "Base", "Documentos", "Conduta", "Pré", "Consequências", "Norma", "Modalidade", "Etapa", "Tipo", "Documento", "Verificação", "Etapas", "Resultado", "Onde", "Como", "Fiscalização")):
                if len(chunk[i+1]) > 50 or "NOVIDADE" in p or "PRAZO" in p or "PROTOCOLO" in p or "NUNCA" in p or "FISCALIZAÇÃO" in p or "VALIDADE" in p or "CRUZAMENTO" in p:
                    body = f'<p>{esc(chunk[i+1])}</p>'
                    i += 1
            cls = callout(p).split('"')[1] if '"' in callout(p) else "callout info"
            kind = {"★": "highlight", "⚠": "warning", "ℹ": "info", "✔": "tip"}.get(p[0], "info")
            out.append(f'<div class="callout {kind}">{esc(p)}{body}</div>')
            i += 1
            continue

        if p == "Modalidade":
            out.append('<h3>Modalidades para Postos em SP</h3>')
            out.append(render_table(
                ["Modalidade", "AVCB-PTS (Projeto Simplificado)", "AVCB-PT (Projeto Completo)"],
                [
                    ["Quando usar", "Área construída até 750 m²", "Área acima de 750 m² ou risco elevado"],
                    ["Cobertura das bombas", "Pode ser desconsiderada na área computada desde que atenda a critérios técnicos específicos – consultar IT vigente para verificar enquadramento.", ""],
                ]
            ))
            i += 1
            while i < len(chunk) and chunk[i] in ("Modalidade", "AVCB-PTS (Projeto Simplificado)", "AVCB-PT (Projeto Completo)", "Quando usar", "Área construída até 750 m²", "Área acima de 750 m² ou risco elevado", "Cobertura das bombas", "Pode ser desconsiderada na área computada desde que atenda a critérios técnicos específicos – consultar IT vigente para verificar enquadramento."):
                i += 1
            continue

        if p == "Irregularidade":
            rows = []
            j = i + 2
            while j + 1 < len(chunk) and not chunk[j].startswith("★"):
                rows.append([chunk[j], chunk[j+1]])
                j += 2
            out.append(f'<h3>Consequências da Irregularidade</h3>')
            out.append(render_table(["Irregularidade", "Consequência"], rows))
            i = j
            continue

        if p == "Etapa":
            rows = []
            j = i + 2
            while j + 1 < len(chunk) and chunk[j].startswith(("1", "2", "3")):
                rows.append([chunk[j], chunk[j+1]])
                j += 2
            out.append('<h3>Etapas do Ensaio</h3>')
            out.append(render_table(["Etapa", "Procedimento"], rows))
            i = j
            continue

        if p == "Tipo" and i + 1 < len(chunk) and chunk[i+1] == "Quando e como ocorre":
            rows = []
            j = i + 2
            while j + 1 < len(chunk) and chunk[j].startswith(("Verificação", "Verificação")):
                rows.append([chunk[j], chunk[j+1]])
                j += 2
            out.append('<h3>Verificação Metrológica das Bombas – IPEM-SP / INMETRO 2026</h3>')
            out.append(render_table(["Tipo", "Quando e como ocorre"], rows))
            i = j
            continue

        if p == "Documento" and i + 2 < len(chunk) and chunk[i+1] == "Órgão":
            rows = []
            j = i + 3
            while j + 2 < len(chunk) and chunk[j] not in ("Fiscalização", "★"):
                rows.append([chunk[j], chunk[j+1], chunk[j+2]])
                j += 3
            out.append('<h3>Documentos que Devem Estar no Posto para a ANP</h3>')
            out.append(render_table(["Documento", "Órgão", "Validade"], rows))
            i = j
            continue

        # Section headers followed by list items
        LIST_HEADERS = (
            "Documentos Exigidos para Emissão / Renovação",
            "Documentos Exigidos na Renovação (versão agosto/2025 – CETESB)",
            "Pré-requisitos para Emissão / Renovação",
            "Documentação Exigida no Cadastro Municipal (SMUL)",
            "Condicionantes Mais Comuns na LO de Postos em SP",
            "Consequências da Irregularidade",
            "O que o Laudo Deve Cobrir",
            "Onde o Laudo Deve Estar",
            "O que Deve Estar Atualizado na FAC",
            "Fiscalização da ANP em Campo",
            "Conduta em Vistoria do Bombeiro",
            "Conduta em Vistoria do IPEM",
            "Normas Técnicas de Referência",
            "Como Atualizar",
            "Comprovantes de implantação dos sistemas de combate a incêndio:",
        )
        if p in LIST_HEADERS or p.startswith("Verificação Metrológica"):
            title = p if not p.startswith("Verificação") else p
            if p.startswith("Verificação"):
                out.append(f'<h3>{esc(p)}</h3>')
                i += 1
                continue
            out.append(f'<h3>{esc(p)}</h3><ul>')
            i += 1
            while i < len(chunk):
                cur = chunk[i]
                if cur in LIST_HEADERS or cur == "O que é?" or cur.startswith(("★", "⚠", "ℹ", "Norma", "Irregularidade", "Modalidade", "Etapa", "Tipo", "Documento", "Verificação", "★  O QUE")):
                    break
                out.append(f'<li>{esc(cur)}</li>')
                i += 1
            out.append('</ul>')
            continue

        out.append(f'<p>{esc(p)}</p>')
        i += 1

    return "\n".join(out)

HTML_TEMPLATE = open(f"{BASE}/template.html", encoding="utf-8").read() if False else """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Treinamento — Postos de Combustíveis</title>
  <style>
    :root {{
      --bg: #f4f6f9; --surface: #fff; --text: #1a2332; --muted: #5c6b7a;
      --primary: #1e4d8c; --primary-light: #e8f0fa; --accent: #e85d04;
      --shadow: 0 2px 12px rgba(0,0,0,.08); --radius: 10px;
    }}
    * {{ box-sizing: border-box; margin: 0; padding: 0; }}
    body {{ font-family: 'Segoe UI', system-ui, sans-serif; background: var(--bg); color: var(--text); line-height: 1.65; font-size: 16px; }}
    header.site-header {{ background: linear-gradient(135deg, #1e4d8c, #163a6b); color: #fff; padding: 2rem 1.5rem; text-align: center; }}
    header.site-header h1 {{ font-size: 1.75rem; margin-bottom: .5rem; }}
    header.site-header p {{ opacity: .9; max-width: 640px; margin: 0 auto; }}
    nav.tabs {{ display: flex; justify-content: center; gap: .5rem; padding: 1rem; background: var(--surface); border-bottom: 1px solid #dde3ea; position: sticky; top: 0; z-index: 100; flex-wrap: wrap; }}
    nav.tabs button {{ padding: .65rem 1.25rem; border: 2px solid var(--primary); background: transparent; color: var(--primary); border-radius: 999px; cursor: pointer; font-weight: 600; transition: all .2s; }}
    nav.tabs button:hover, nav.tabs button.active {{ background: var(--primary); color: #fff; }}
    main {{ max-width: 900px; margin: 0 auto; padding: 2rem 1.25rem 4rem; }}
    .panel {{ display: none; }} .panel.active {{ display: block; }}
    .panel-header {{ background: var(--surface); border-radius: var(--radius); padding: 1.75rem; margin-bottom: 1.5rem; box-shadow: var(--shadow); border-left: 5px solid var(--accent); }}
    .panel-header h2 {{ color: var(--primary); font-size: 1.5rem; }}
    .panel-header .meta {{ color: var(--muted); font-size: .9rem; }}
    .products-tag {{ display: flex; flex-wrap: wrap; gap: .4rem; margin-top: 1rem; }}
    .products-tag span {{ background: var(--primary-light); color: var(--primary); padding: .25rem .65rem; border-radius: 6px; font-size: .8rem; font-weight: 600; }}
    .golden-rule {{ background: linear-gradient(135deg, #fff8e7, #fff3cd); border: 2px solid #f0a500; border-radius: var(--radius); padding: 1.25rem 1.5rem; margin-bottom: 1.5rem; }}
    .golden-rule h3 {{ color: #b8860b; margin-bottom: .5rem; }}
    .module {{ background: var(--surface); border-radius: var(--radius); padding: 1.5rem 1.75rem; margin-bottom: 1.25rem; box-shadow: var(--shadow); }}
    .module h2 {{ color: var(--primary); font-size: 1.25rem; margin-bottom: 1rem; padding-bottom: .5rem; border-bottom: 2px solid var(--primary-light); }}
    .module h3 {{ font-size: 1.05rem; margin: 1.25rem 0 .6rem; }}
    .module h4 {{ font-size: .95rem; margin-bottom: .5rem; color: var(--primary); }}
    .module p {{ margin-bottom: .75rem; }}
    .module li {{ margin: .35rem 0 .35rem 1.25rem; }}
    table {{ width: 100%; border-collapse: collapse; margin: 1rem 0; font-size: .9rem; }}
    th, td {{ border: 1px solid #dde3ea; padding: .6rem .75rem; text-align: left; vertical-align: top; }}
    th {{ background: var(--primary-light); color: var(--primary); font-weight: 600; }}
    tr:nth-child(even) td {{ background: #fafbfc; }}
    .callout {{ border-radius: 8px; padding: 1rem 1.15rem; margin: 1rem 0; font-size: .92rem; }}
    .callout.warning {{ background: #fff3cd; border-left: 4px solid #ffc107; }}
    .callout.info {{ background: #d1ecf1; border-left: 4px solid #17a2b8; }}
    .callout.highlight {{ background: #fff8e7; border-left: 4px solid #f0a500; }}
    .callout.tip {{ background: #d4edda; border-left: 4px solid #2d6a4f; }}
    .hero-gerentes {{ background: linear-gradient(135deg, #1e4d8c, #2e6cb5); color: #fff; border-radius: var(--radius); padding: 2rem; margin-bottom: 1.5rem; text-align: center; }}
    .hero-gerentes h2 {{ font-size: 1.4rem; line-height: 1.4; margin: .5rem 0; }}
    .hero-gerentes .eyebrow {{ text-transform: uppercase; letter-spacing: .1em; font-size: .8rem; opacity: .85; }}
    .hero-gerentes .version {{ opacity: .8; font-size: .85rem; margin-top: .75rem; }}
    .objective-box {{ background: var(--surface); border-radius: var(--radius); padding: 1.5rem; margin-bottom: 1.25rem; box-shadow: var(--shadow); }}
    .objective-box h3 {{ color: var(--primary); margin-bottom: .5rem; }}
    .objective-box .orgs {{ margin-top: .75rem; font-size: .9rem; color: var(--muted); }}
    .module-toc {{ background: var(--surface); border-radius: var(--radius); padding: 1.25rem 1.5rem; margin-bottom: 1.25rem; box-shadow: var(--shadow); }}
    .module-toc a {{ color: var(--primary); text-decoration: none; }}
    .module-toc a:hover {{ text-decoration: underline; }}
    .module-sub {{ color: var(--muted); font-size: .95rem; margin-top: -.5rem; margin-bottom: 1rem; }}
    .key-points {{ background: #f0f7ff; border-radius: 8px; padding: 1rem 1.25rem; margin: 1rem 0; }}
    .executive-summary table {{ font-size: .82rem; }}
    .footer-note {{ font-weight: 600; color: var(--primary); margin-top: 1rem; }}
    .doc-footer {{ text-align: center; color: var(--muted); font-size: .85rem; margin-top: 2rem; font-style: italic; }}
    @media print {{ nav.tabs {{ display: none; }} .panel {{ display: block !important; page-break-before: always; }} }}
    @media (max-width: 600px) {{ table {{ font-size: .78rem; }} th, td {{ padding: .4rem .5rem; }} }}
  </style>
</head>
<body>
  <header class="site-header">
    <h1>Treinamento — Postos de Combustíveis</h1>
    <p>Material de capacitação para frentistas e gerentes. Fluidos automotivos e documentação regulatória.</p>
  </header>
  <nav class="tabs" role="tablist">
    <button class="active" data-tab="fluidos" role="tab">Fluidos Automotivos</button>
    <button data-tab="gerentes" role="tab">Documentação Regulatória</button>
  </nav>
  <main>
    <div id="fluidos" class="panel active" role="tabpanel">
      <div class="panel-header">
        <h2>Fluidos Automotivos</h2>
        <p class="meta">Para Frentistas e Gerentes</p>
        <div class="products-tag">
          <span>DOT 3</span><span>DOT 4</span><span>ATF</span><span>5W-30</span><span>0W-20</span><span>15W-40</span><span>20W-50</span>
        </div>
      </div>
      {fluidos_content}
    </div>
    <div id="gerentes" class="panel" role="tabpanel">
      {gerentes_content}
    </div>
  </main>
  <script>
    document.querySelectorAll('nav.tabs button').forEach(btn => {{
      btn.addEventListener('click', () => {{
        document.querySelectorAll('nav.tabs button').forEach(b => b.classList.remove('active'));
        document.querySelectorAll('.panel').forEach(p => p.classList.remove('active'));
        btn.classList.add('active');
        document.getElementById(btn.dataset.tab).classList.add('active');
        window.scrollTo({{ top: 0, behavior: 'smooth' }});
      }});
    }});
  </script>
</body>
</html>"""

def main():
    with open(f"{BASE}/extracted_content.json", encoding="utf-8") as f:
        data = json.load(f)

    html_out = HTML_TEMPLATE.format(
        fluidos_content=render_fluidos(data["treinamento-fluidos-v2.docx"]),
        gerentes_content=render_gerentes(data["Treinamento_Gerentes_Postos_2026.docx"]),
    )

    out_path = f"{BASE}/index.html"
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html_out)
    print(f"Generated: {out_path} ({len(html_out)} bytes)")

if __name__ == "__main__":
    main()
