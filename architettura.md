# Architettura – Penumbra v20 (post step 3.3)

## Restore flow (invariato nel flusso, arricchito nei dati)

1. Client ha `game_id` (localStorage / query)
2. `GET /api/state?game_id=`
3. Se non in `_games` → `supabase_store.fetch_game`
4. `hydrate(state_json)` ricostruisce `GameState`
5. Partita torna giocabile

### Cosa fa ora `hydrate` (v20)

1. Crea `GameState` (layout board fisso dal costruttore)
2. Pulisce unità / mani / corona
3. Applica turn, phase, current_player, winner, main_quest, log
4. Ripristina player (mana, hand, fragments, is_ai, …)
5. **NEW** Ripristina **tile** da ogni cella di `board[][]`:
   - `tile` → `tile_type` (se valore enum valido)
   - `explored`
   - `permanent_effect` (se presente)
   - `trap_card_id` (se presente)
   - `wall_hp` (se presente)
   - `owner_id` (se presente)
6. Ripristina unità sulla board
7. Ripristina pool Eldrazi (best effort per nome)

File coinvolti:
- `api/restore.py` – `hydrate()`
- `api/main.py` – `serialize_state()` (campi tile ricchi)
- `api/supabase_store.py` – invariato (salva l’intero `state_json`)

## Snapshot board (cell)

Campi **sempre** presenti (già da v9+):

- `coord`, `tile`, `explored`, `trap` (bool), `ritual`, `altar`, `unit`

Campi **nuovi** (v20, opzionali in lettura):

- `permanent_effect: str | null`
- `trap_card_id: int | null`
- `wall_hp: int`
- `owner_id: int | null`

I client vecchi che ignorano i campi extra non si rompono.

## Limiti ancora aperti

- **Status temporanei** sulle unità (`unit.statuses`) non sono ancora nello snapshot → al restore si perdono buff/debuff a tempo.
- Eventi esplorati: ora il **tipo tile** e `explored` + `permanent_effect` vengono ripristinati; se in futuro un evento scrive altri flag custom, vanno aggiunti esplicitamente.
- Draft in corso: lo snapshot include già `draft` lato serialize; hydrate non ricostruisce ancora i pack draft (partita in DRAFT dopo sleep resta fragile).

## Prossimi (architetturali)

1. Snapshot status unità (e eventuali contatori turno)
2. Realtime Supabase (presenza / sync PvP)
3. Auth
4. Snapshot draft completo se si vuole restore a metà draft

**Versione API: 0.20 · Step roadmap: 3.3 fatto**
