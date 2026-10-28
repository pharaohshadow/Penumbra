# Architettura – v1.14

## Stato attuale

Nuova tattica per le montagne (richiesta utente):

- Le montagne esistono **solo nei corridoi tra gli esagoni** (SVG sotto le caselle).
- Corridoio **marrone** = montagna (ostacolo).
- Corridoio **verdino** = passabile (stesso colore degli esagoni).
- Corridoio **rosso** = bordo esterno (al posto della sola “lava” come linea di separazione).

Gli esagoni restano sopra: così il colore del corridoio non entra mai nel centro della casella.

### File toccati
- `backend/static/index.html`

### Render
- URL live: https://penumbra-8psb.onrender.com
