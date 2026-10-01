# Hub de tableros Gerencia T&D

Portal en Streamlit con acceso a las aplicaciones Qlik Sense de la Gerencia T&D Energía (EPM).

## Ejecutar en local

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Agregar o editar tableros

Edita `aplicaciones.json`. Cada tablero tiene:

```json
{
    "categoria": "Operación",
    "app": "Nombre del tablero",
    "descripcion": "Qué se consulta en el tablero.",
    "url": "https://autoqlik.epm.com.co/sense/app/..."
}
```

Las categorías nuevas aparecen solas en los filtros. Si quieres un icono propio para una categoría nueva, agrégalo en el diccionario `ICONOS` de `app.py`.

## Publicar en Streamlit Community Cloud

1. Sube esta carpeta a un repositorio de GitHub (`app.py`, `aplicaciones.json`, `EPM.png`, `requirements.txt`, `.streamlit/config.toml`).
2. En https://share.streamlit.io elige *New app*, selecciona el repositorio y como archivo principal `app.py`.
