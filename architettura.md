# Architettura – v1.0

## Stato attuale (ottobre 2026)

Il progetto è in **fase di transizione** dalla vecchia griglia quadrata 5×5 alla nuova **mappa esagonale**.

### Mappa
- File di definizione: `backend/data/map.json`
- Tipo: esagonale (coordinate assiali q,r)
- radius: 5
- playable_radius: 4
- 4 templi (temple1 → temple4)
- Altare centrale in (0,0)
- Cornice (`frame`) non walkable
- Muri definiti come connessioni tra celle (non più tile intere)

### Backend
- FastAPI
- Cartella principale: `backend/`
- Core: `core/` (game_state, map_board, unit, tile, card, constants, player)
- AI: `ai/basic_ai.py`
- Persistenza: Supabase (opzionale, se configurato)
- Deploy: Render (file `render.yaml` nella root)

### Frontend
- File unico: `backend/static/index.html`
- Attualmente ancora basato sulla griglia 5×5 (CSS grid)
- Autenticazione Supabase integrata

### Supabase
- URL: `https://favrmxwyaxklfiruyvqz.supabase.co`
- Anon key: presente nel frontend (`index.html`)
- JWT Secret e Service Key: da configurare nelle variabili d’ambiente di Render

### Render
- Servizio: `penumbra-backend`
- Runtime: Python 3.12.3
- Root directory: `backend`
- Start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

### Note importanti
- La logica di gioco (`GameState`, movimento, spawn, ecc.) è ancora legata alla 5×5.
- La migrazione completa alla mappa esagonale è il lavoro principale della versione 1.x.
- In v1.0 sono stati introdotti i primi moduli del nuovo sistema esagonale (`hex_coords.py`, aggiornamenti a `constants.py` e `map_board.py`).
