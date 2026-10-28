# Architettura – v1.6

## Stato attuale

Fix del 28/10/2026 (dopo v1.5):
Aggiunta la funzione `hex_to_pixel` in `constants.py`.

Errore che bloccava Render:
```
ImportError: cannot import name 'hex_to_pixel' from 'core.constants'
```

`api/main.py` la usa per calcolare le coordinate pixel della mappa esagonale da inviare alla UI.

### Import supportati in constants.py
- HEX_RADIUS, PLAYABLE_RADIUS
- HexPos, hex_neighbors, hex_in_radius, all_hexes, hex_key, hex_distance
- parse_hex_key (da v1.5)
- **hex_to_pixel** (nuovo in v1.6)
- ALTAR_POS, TEMPLE_P1_POS … TEMPLE_P4_POS
- FLAVOR_NAMES, TileType, load_user_map
- GRID_SIZE, pos_to_coord, coord_to_pos (legacy 5×5)

### Supabase
- URL: `https://favrmxwyaxklfiruyvqz.supabase.co`

### Render
- Servizio: penumbra-backend
- URL live: https://penumbra-8psb.onrender.com
- Root directory: `backend`
- Start command: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
- Nota: il log di Render mostra ancora Python 3.14.8 invece di 3.12.3.
  Se si vuole forzare la versione: Environment → PYTHON_VERSION = 3.12.3
