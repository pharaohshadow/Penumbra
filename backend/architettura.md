# Architettura – Penumbra v9

## Restore flow

1. Client ha `game_id` in localStorage / query
2. `GET /api/state?game_id=`
3. Se non in `_games` → `supabase_store.fetch_game`
4. `hydrate(state_json)` ricostruisce `GameState` (unità, mani, mana, turno, quest, eldrazi)
5. Partita torna giocabile

File nuovi/modificati:
- `api/restore.py` – `hydrate()`
- `api/supabase_store.py` – `fetch_game()`, `create_game(..., game_id=)`
- `api/main.py` – `_load_from_supabase`, `_require_game`

## Limiti hydrate
- Effetti status temporanei sulle unità non sono nello snapshot leggero
- Tessere evento esplorate: tipo tile nello snapshot board (etichetta), non tutti i permanent_effect
- Sufficiente per continuare una partita dopo sleep

## Prossimi
1. Snapshot più ricco (tile types completi)
2. Realtime Supabase
3. Auth

**Versione: v9**
