# Architettura – Penumbra v6

## Stack

| Layer | Tecnologia |
|-------|------------|
| Motore + IA | Python `core/`, `ai/` |
| API + UI | FastAPI + `static/index.html` |
| Hosting | Render |
| DB (opzionale) | Supabase (Postgres + REST) |
| Docs | GitHub Pages `/docs` |

## Persistenza

- Senza env Supabase → solo memoria processo (come v5)
- Con `SUPABASE_URL` + `SUPABASE_ANON_KEY`:
  - `create_game` a inizio partita
  - `update_game` dopo ogni mossa / fine turno
  - `log_move` su `game_moves`

File: `api/supabase_store.py`  
Schema: `supabase/schema.sql`

## Flusso

1. Browser → Render URL
2. `GET /api/state` (crea partita se serve)
3. Mosse → `_persist()`
4. `POST /api/end` → IA → `_persist()`

## Sicurezza attuale

RLS aperta in anon per prototipo. Prima di PvP pubblico: auth Supabase + policy per `user_id`.

## Prossimi passi

1. Auth + due giocatori umani sulla stessa `game_id`
2. Realtime Supabase (subscription su `games`)
3. Ripristino stato da `state_json` dopo sleep Render

**Versione: v6**
