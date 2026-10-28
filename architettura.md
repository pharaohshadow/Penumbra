# Architettura – v1.1

## Stato attuale (ottobre 2026)

Il progetto è in **fase di stabilizzazione** dopo errori di importazione causati da versioni miste di `map_board.py` e `constants.py`.

### Problema risolto in v1.1
`map_board.py` presente sul server Render richiedeva funzioni esagonali (`HexPos`, `hex_neighbors`, `hex_in_radius`, ecc.) non presenti in `constants.py`.  
In questa versione `constants.py` è stato reso **pienamente compatibile** con tutte le richieste osservate.

### Mappa
- File di definizione: `backend/data/map.json`
- Tipo: esagonale (coordinate assiali q,r)
- radius: 5 / playable_radius: 4
- 4 templi + altare centrale
- Muri tra celle

### Backend
- FastAPI
- Core: `core/`
- Deploy: Render

### Supabase
- URL: `https://favrmxwyaxklfiruyvqz.supabase.co`
- Anon key: presente nel frontend

### Render
- Servizio: `penumbra-backend`
- Runtime: Python 3.12+ / 3.14
- Root directory: `backend`
