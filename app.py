"""Hub de tableros Gerencia T&D — portal de acceso a las aplicaciones Qlik Sense."""

import base64
import json
import unicodedata
from html import escape
from pathlib import Path

import streamlit as st

BASE_DIR = Path(__file__).parent
LOGO_PATH = BASE_DIR / "EPM.png"
DATA_PATH = BASE_DIR / "aplicaciones.json"

TITULO = "Hub de tableros Gerencia T&D"
SUBTITULO = "Gerencia Transmisión y Distribución Energía"
TODAS = "Todas"

# Icono (SVG de trazo) por categoría; las categorías nuevas usan el de "default".
ICONOS = {
    "Operación": '<path d="M13 2 4 14h7l-1 8 9-12h-7l1-8z"/>',
    "Indicadores": '<path d="M3 3v18h18"/><path d="M7 15l4-4 3 3 5-6"/>',
    "Calidad de Datos": '<path d="M12 3 4 6v6c0 5 3.5 8 8 9 4.5-1 8-4 8-9V6l-8-3z"/><path d="m9 12 2 2 4-4"/>',
    "default": '<rect x="3" y="3" width="7" height="7" rx="1.5"/><rect x="14" y="3" width="7" height="7" rx="1.5"/>'
    '<rect x="3" y="14" width="7" height="7" rx="1.5"/><rect x="14" y="14" width="7" height="7" rx="1.5"/>',
}

st.set_page_config(
    page_title=TITULO,
    page_icon=str(LOGO_PATH),
    layout="wide",
    initial_sidebar_state="collapsed",
)


@st.cache_data
def cargar_aplicaciones() -> list[dict]:
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


@st.cache_data
def logo_base64() -> str:
    return base64.b64encode(LOGO_PATH.read_bytes()).decode()


def normalizar(texto: str) -> str:
    """Minúsculas y sin tildes, para que 'operacion' encuentre 'Operación'."""
    sin_tildes = unicodedata.normalize("NFKD", texto)
    return "".join(c for c in sin_tildes if not unicodedata.combining(c)).lower()


def icono(categoria: str, tamano: int = 22) -> str:
    trazos = ICONOS.get(categoria, ICONOS["default"])
    return (
        f'<svg width="{tamano}" height="{tamano}" viewBox="0 0 24 24" fill="none" stroke="currentColor" '
        f'stroke-width="2" stroke-linecap="round" stroke-linejoin="round">{trazos}</svg>'
    )


CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:opsz,wght@6..12,400;6..12,600;6..12,700;6..12,800&display=swap');

:root {
    --epm-verde: #00843D;
    --epm-verde-osc: #005F2C;
    --epm-lima: #8DC63F;
    --epm-claro: #EAF5EF;
    --fondo: #F4F7F5;
    --texto: #1F2D25;
    --gris: #5F6B64;
    --borde: #DCE5DF;
}

html, body, [class*="st-"], .stApp, button, input {
    font-family: "Nunito Sans", "Segoe UI", Arial, sans-serif;
}

/* Ocultar el chrome de Streamlit para un look de portal */
#MainMenu, footer, [data-testid="stToolbar"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], header[data-testid="stHeader"] {
    display: none !important;
}

.stApp { background: var(--fondo); }
.block-container {
    padding-top: 1.5rem !important;
    padding-bottom: 2rem !important;
    max-width: 1240px;
}

/* ---------- Encabezado ---------- */
.hub-header {
    background: #FFFFFF;
    border: 1px solid var(--borde);
    border-radius: 18px;
    overflow: hidden;
    box-shadow: 0 6px 24px rgba(0, 95, 44, .08);
    margin-bottom: 1.25rem;
}
.hub-header-top {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 1.5rem;
    flex-wrap: wrap;
    padding: 1.5rem 2rem;
}
.hub-brand {
    display: flex;
    align-items: center;
    gap: 1.4rem;
}
.hub-brand img {
    height: 54px;
    width: auto;
}
.hub-divider {
    width: 2px;
    height: 54px;
    background: linear-gradient(180deg, var(--epm-verde), var(--epm-lima));
    border-radius: 2px;
}
.hub-brand h1 {
    margin: 0 !important;
    padding: 0 !important;
    font-size: clamp(1.5rem, 2.6vw, 2.1rem) !important;
    font-weight: 800 !important;
    color: var(--epm-verde-osc) !important;
    line-height: 1.15 !important;
}
.hub-brand p {
    margin: .25rem 0 0 !important;
    color: var(--gris);
    font-size: 1rem;
}
.hub-stats {
    display: flex;
    gap: .75rem;
}
.hub-stat {
    background: var(--epm-claro);
    border-radius: 12px;
    padding: .6rem 1.1rem;
    text-align: center;
    min-width: 96px;
}
.hub-stat strong {
    display: block;
    font-size: 1.6rem;
    font-weight: 800;
    color: var(--epm-verde);
    line-height: 1.1;
}
.hub-stat span {
    font-size: .78rem;
    color: var(--gris);
    text-transform: uppercase;
    letter-spacing: .04em;
}
.hub-header-bar {
    height: 6px;
    background: linear-gradient(90deg, var(--epm-verde-osc), var(--epm-verde) 45%, var(--epm-lima));
}

/* ---------- Barra de búsqueda y filtros ---------- */
.stTextInput input {
    border-radius: 12px !important;
    padding: .8rem 1rem !important;
    font-size: 1rem !important;
    background: #FFFFFF !important;
}
.stTextInput div[data-baseweb="input"] {
    border-radius: 12px !important;
    border: 1px solid var(--borde) !important;
    background: #FFFFFF !important;
}
.stTextInput div[data-baseweb="input"]:focus-within {
    border-color: var(--epm-verde) !important;
    box-shadow: 0 0 0 3px rgba(0, 132, 61, .12) !important;
}

/* ---------- Secciones y tarjetas ---------- */
.hub-section {
    display: flex;
    align-items: center;
    gap: .7rem;
    margin: 1.6rem 0 .9rem;
}
.hub-section-icon {
    display: grid;
    place-items: center;
    width: 38px;
    height: 38px;
    border-radius: 10px;
    background: var(--epm-verde);
    color: #FFFFFF;
}
.hub-section h2 {
    margin: 0 !important;
    padding: 0 !important;
    font-size: 1.3rem !important;
    font-weight: 800 !important;
    color: var(--epm-verde-osc) !important;
}
.hub-section .hub-count {
    margin-left: auto;
    font-size: .85rem;
    color: var(--gris);
}
.hub-section-line {
    flex: 1;
    height: 1px;
    background: var(--borde);
}

.hub-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
    gap: 1rem;
}
a.hub-card, a.hub-card:hover, a.hub-card:visited {
    text-decoration: none !important;
    color: inherit !important;
}
.hub-card {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: .55rem;
    background: #FFFFFF;
    border: 1px solid var(--borde);
    border-radius: 14px;
    padding: 1.2rem 1.3rem 1.1rem;
    box-shadow: 0 2px 8px rgba(25, 55, 40, .05);
    transition: transform .18s ease, box-shadow .18s ease, border-color .18s ease;
    overflow: hidden;
}
.hub-card::before {
    content: "";
    position: absolute;
    inset: 0 0 auto 0;
    height: 4px;
    background: linear-gradient(90deg, var(--epm-verde), var(--epm-lima));
    transform: scaleX(0);
    transform-origin: left;
    transition: transform .25s ease;
}
.hub-card:hover {
    transform: translateY(-3px);
    border-color: rgba(0, 132, 61, .35);
    box-shadow: 0 10px 24px rgba(0, 95, 44, .12);
}
.hub-card:hover::before { transform: scaleX(1); }
.hub-card-head {
    display: flex;
    align-items: flex-start;
    gap: .8rem;
}
.hub-card-icon {
    flex: none;
    display: grid;
    place-items: center;
    width: 40px;
    height: 40px;
    border-radius: 50%;
    background: var(--epm-claro);
    color: var(--epm-verde);
}
.hub-card h3 {
    margin: 0 !important;
    padding: .1rem 0 0 !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    color: var(--texto) !important;
    line-height: 1.3 !important;
}
.hub-card p {
    margin: 0 !important;
    color: var(--gris);
    font-size: .92rem;
    line-height: 1.45;
    flex: 1;
}
.hub-card-cta {
    display: inline-flex;
    align-items: center;
    gap: .4rem;
    align-self: flex-start;
    margin-top: .3rem;
    padding: .45rem .9rem;
    border-radius: 8px;
    background: var(--epm-verde);
    color: #FFFFFF;
    font-weight: 700;
    font-size: .88rem;
    transition: background .18s ease, gap .18s ease;
}
.hub-card:hover .hub-card-cta {
    background: var(--epm-verde-osc);
    gap: .7rem;
}

.hub-empty {
    text-align: center;
    background: #FFFFFF;
    border: 1px dashed var(--borde);
    border-radius: 14px;
    padding: 2.5rem 1rem;
    color: var(--gris);
    margin-top: 1.5rem;
}
.hub-empty strong {
    display: block;
    color: var(--texto);
    font-size: 1.1rem;
    margin-bottom: .3rem;
}

.hub-footer {
    margin-top: 3rem;
    padding-top: 1.2rem;
    border-top: 1px solid var(--borde);
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: .75rem;
    color: var(--gris);
    font-size: .85rem;
}
.hub-footer img { height: 26px; opacity: .85; }

@media (max-width: 720px) {
    .hub-header-top { padding: 1.2rem; }
    .hub-brand { gap: .9rem; }
    .hub-brand img { height: 40px; }
    .hub-divider { height: 40px; }
    .hub-stats { width: 100%; }
    .hub-stat { flex: 1; }
    .hub-grid { grid-template-columns: 1fr; }
}
</style>
"""


def render_header(total_apps: int, total_categorias: int, logo: str) -> None:
    st.markdown(
        f"""
<div class="hub-header">
<div class="hub-header-top">
<div class="hub-brand">
<img src="data:image/png;base64,{logo}" alt="EPM">
<div class="hub-divider"></div>
<div>
<h1>{escape(TITULO)}</h1>
<p>{escape(SUBTITULO)} · Acceso a las aplicaciones analíticas en Qlik Sense</p>
</div>
</div>
<div class="hub-stats">
<div class="hub-stat"><strong>{total_apps}</strong><span>Tableros</span></div>
<div class="hub-stat"><strong>{total_categorias}</strong><span>Categorías</span></div>
</div>
</div>
<div class="hub-header-bar"></div>
</div>
""",
        unsafe_allow_html=True,
    )


def render_tarjeta(app: dict) -> str:
    return (
        f'<a class="hub-card" href="{escape(app["url"])}" target="_blank" rel="noopener noreferrer">'
        f'<div class="hub-card-head">'
        f'<div class="hub-card-icon">{icono(app["categoria"], 20)}</div>'
        f'<h3>{escape(app["app"])}</h3>'
        f"</div>"
        f'<p>{escape(app["descripcion"])}</p>'
        f'<span class="hub-card-cta">Abrir tablero <span>→</span></span>'
        f"</a>"
    )


def render_categoria(categoria: str, apps: list[dict]) -> None:
    n = len(apps)
    tarjetas = "".join(render_tarjeta(a) for a in apps)
    st.markdown(
        f'<div class="hub-section">'
        f'<div class="hub-section-icon">{icono(categoria)}</div>'
        f"<h2>{escape(categoria)}</h2>"
        f'<div class="hub-section-line"></div>'
        f'<span class="hub-count">{n} tablero{"" if n == 1 else "s"}</span>'
        f"</div>"
        f'<div class="hub-grid">{tarjetas}</div>',
        unsafe_allow_html=True,
    )


def main() -> None:
    st.markdown(CSS, unsafe_allow_html=True)

    aplicaciones = cargar_aplicaciones()
    logo = logo_base64()
    categorias = sorted({a["categoria"] for a in aplicaciones}, key=normalizar)

    render_header(len(aplicaciones), len(categorias), logo)

    col_buscar, col_filtro = st.columns([3, 2], vertical_alignment="center")
    with col_buscar:
        busqueda = st.text_input(
            "Buscar",
            placeholder="🔍  Buscar tablero por nombre, descripción o categoría…",
            label_visibility="collapsed",
        )
    with col_filtro:
        categoria_sel = st.pills(
            "Categoría",
            [TODAS, *categorias],
            default=TODAS,
            label_visibility="collapsed",
        ) or TODAS

    texto = normalizar(busqueda.strip())
    filtradas = [
        a
        for a in aplicaciones
        if (categoria_sel == TODAS or a["categoria"] == categoria_sel)
        and (
            not texto
            or texto in normalizar(a["app"])
            or texto in normalizar(a["descripcion"])
            or texto in normalizar(a["categoria"])
        )
    ]

    if not filtradas:
        st.markdown(
            '<div class="hub-empty"><strong>No se encontraron tableros</strong>'
            "Prueba con otra palabra o selecciona otra categoría.</div>",
            unsafe_allow_html=True,
        )
    else:
        for categoria in categorias:
            apps = sorted((a for a in filtradas if a["categoria"] == categoria), key=lambda a: normalizar(a["app"]))
            if apps:
                render_categoria(categoria, apps)

    st.markdown(
        f'<div class="hub-footer">'
        f"<span>{escape(TITULO)} · Las aplicaciones abren en Qlik Sense y requieren conexión a la red corporativa EPM.</span>"
        f'<img src="data:image/png;base64,{logo}" alt="EPM">'
        f"</div>",
        unsafe_allow_html=True,
    )


main()
