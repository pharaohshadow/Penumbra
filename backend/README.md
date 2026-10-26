# Penumbra – Tactical Card Game 5×5 (v7)

UI web + IA + **partite multiple** + **base PvP** (host / join).

## Online

Dopo il redeploy su Render, apri l’URL del servizio.

### Vs IA
- **Nuova vs IA** → giochi contro l’AI (P0 in basso)

### PvP (due umani, stessa istanza Render)
1. Host: **Nuova PvP (host)** → copia il `game_id` mostrato
2. Guest: **Unisciti** → incolla il `game_id`
3. Host è P0 (basso), Guest è P1 (alto)
4. A turno: mosse + **Fine turno** (niente IA)

> Piano free Render: se il servizio va in sleep, le partite in RAM si perdono. Con Supabase le righe restano in DB (ripristino completo in una prossima versione).

## API nuove / aggiornate

| Metodo | Path | Body |
|--------|------|------|
| POST | `/api/new` | `{vs_ai, name}` |
| POST | `/api/join` | `{game_id, name}` |
| GET | `/api/state?game_id=` | |
| POST | `/api/move` | `{game_id, from_coord, to_coord, player_id}` |
| POST | `/api/play` | `{game_id, hand_index, target_coord?, player_id}` |
| POST | `/api/end` | `{game_id, player_id}` |
| GET | `/api/health` | |

## Deploy

Root Directory `backend` · Build `pip install -r requirements.txt` · Start `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

Vedi **architettura.md**.
