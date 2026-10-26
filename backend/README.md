# Penumbra – Tactical Card Game 5×5 (v6)

Backend + IA + UI web su Render + **Supabase opzionale** (persistenza partite).

## Online (già su Render)

Apri l’URL del Web Service. Funziona anche **senza** Supabase (stato in RAM).

## Attivare Supabase (5 minuti)

1. Crea un progetto su [supabase.com](https://supabase.com)
2. **SQL Editor** → incolla ed esegui `supabase/schema.sql`
3. **Settings → API** → copia:
   - Project URL → `SUPABASE_URL`
   - `anon` `public` key → `SUPABASE_ANON_KEY`
4. Su **Render** → il tuo Web Service → **Environment**:
   - `SUPABASE_URL` = `https://xxxx.supabase.co`
   - `SUPABASE_ANON_KEY` = la anon key
5. **Manual Deploy** / restart del servizio

Da quel momento ogni nuova partita viene scritta nella tabella `games` e le mosse in `game_moves`.

Nella risposta API vedi `"supabase": true` e `"game_id": "..."`.

## Deploy Render (riepilogo)

- Root Directory: `backend`
- Build: `pip install -r requirements.txt`
- Start: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

## File importanti

| Path | Ruolo |
|------|--------|
| `static/index.html` | UI |
| `api/main.py` | FastAPI |
| `api/supabase_store.py` | Persistenza REST |
| `supabase/schema.sql` | Tabelle + RLS |
| `.env.example` | Variabili d’ambiente |

Vedi **`architettura.md`**.
