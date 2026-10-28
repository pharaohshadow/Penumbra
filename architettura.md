# Architettura – v1.8

## Stato attuale

Aggiornamento grafico della mappa (28/10/2026) per avvicinarla allo stile dell’editor muri.

### Cosa è cambiato in `backend/static/index.html`
- Esagoni **flat-top** (come `hex_to_pixel` del backend e l’editor), non più pointy-top
- Colori scuri blu/grigio come nello screenshot “figo”
- Altare giallo, templi verdi, cornice scura senza alberi
- Muri rossi più spessi e allineati ai bordi

### File toccati
- `backend/static/index.html` (solo CSS + pezzi del render mappa)

### Mappa / muri
- `backend/data/map.json` (invariato da v1.7)

### Supabase
- URL: `https://favrmxwyaxklfiruyvqz.supabase.co`

### Render
- URL live: https://penumbra-8psb.onrender.com
