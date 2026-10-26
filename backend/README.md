# Penumbra – Tactical Card Game 5×5 (v9)

## Novità v9
- **Ripristino da Supabase**: se Render va in sleep e perdi la RAM, con `game_id` noto la partita viene ricaricata da `games.state_json`
- `create_game` salva usando lo stesso UUID del client
- `GET /api/state?game_id=` e le mosse tentano prima la memoria, poi Supabase

## Requisiti per il restore
1. Variabili Render: `SUPABASE_URL`, `SUPABASE_ANON_KEY`
2. Schema eseguito (`supabase/schema.sql`)
3. Aver giocato almeno una mossa (così esiste uno snapshot)

Senza Supabase il comportamento resta quello di v8 (solo RAM).

## Online
Redeploy → apri URL → vs IA / PvP come prima.

## Deploy
Root `backend` · `pip install -r requirements.txt` · `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

Vedi **architettura.md**.
