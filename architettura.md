# Architettura – v1.7

## Stato attuale

Aggiornamento muri della mappa esagonale (28/10/2026).

Il file `backend/data/map.json` contiene i muri scelti dall’utente con l’editor HTML.
Le celle (terrain, temple, altar, frame) restano invariate; è cambiata solo la lista `walls`.

### Mappa
- File: `backend/data/map.json`
- Formato muri: `{"a": [q, r], "b": [q, r]}` (bordo tra due esagoni adiacenti)
- Numero muri in questa versione: 55

### Supabase
- URL: `https://favrmxwyaxklfiruyvqz.supabase.co`

### Render
- Servizio: penumbra-backend
- URL live: https://penumbra-8psb.onrender.com
- Root directory: `backend`
- Start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
