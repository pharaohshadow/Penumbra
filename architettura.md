# Architettura – v1.11

## Stato attuale

### Montagne irregolari (roadmap 3.1)
In `backend/static/index.html` gli ostacoli non sono più linee:
- ogni muro è un **poligono SVG** a cresta dentellata
- altezza e numero di picchi variano in modo stabile (seed dalle coordinate)
- colori roccia: base scura, corpo marrone, cresta chiara

Fog of War: ok (fix v1.10).

### File toccati
- `backend/static/index.html` (solo disegno ostacoli)

### Supabase
- URL: `https://favrmxwyaxklfiruyvqz.supabase.co`

### Render
- URL live: https://penumbra-8psb.onrender.com
