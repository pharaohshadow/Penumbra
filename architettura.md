# Architettura – v1.5

## Stato attuale

Fix critico del 28/10/2026: aggiunto `parse_hex_key` in `constants.py`.
Senza questa funzione il deploy su Render falliva con:

```
ImportError: cannot import name 'parse_hex_key' from 'core.constants'
```

Ora `game_state.py` può importare tutto ciò di cui ha bisogno.

### Import supportati in constants.py
- HEX_RADIUS, PLAYABLE_RADIUS
- HexPos, hex_neighbors, hex_in_radius, all_hexes, hex_key, hex_distance
- **parse_hex_key** (nuovo in v1.5)
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
- Nota: il log di Render mostrava Python 3.14.8 invece di 3.12.3.  
  Se si vogliono forzare le versioni, controllare Environment → PYTHON_VERSION = 3.12.3
