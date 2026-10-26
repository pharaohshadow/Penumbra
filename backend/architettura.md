# Architettura – Penumbra v4

## Struttura

```
backend/
├── README.md
├── architettura.md
├── requirements.txt
├── main.py                 # CLI
├── core/                   # Motore puro
├── ai/basic_ai.py          # IA
├── api/main.py             # FastAPI (stato + mosse + serve HTML)
└── static/index.html       # UI browser
```

Repo:
```
Penumbra/
├── backend/   ← questo
└── docs/      ← GitHub Pages (documentazione)
```

## Flusso web

1. Browser apre `/` → `static/index.html`
2. JS chiama `GET /api/state`
3. Utente muove/gioca → `POST /api/move` o `/api/play`
4. Fine turno → `POST /api/end` → server esegue `BasicAI.take_turn()`
5. Risposta = nuovo stato → UI si aggiorna

## File chiave

| File | Ruolo |
|------|--------|
| `api/main.py` | FastAPI, sessione in memoria, `serialize_state`, route |
| `static/index.html` | UI completa (griglia, mano, log, comandi) |
| `core/game_state.py` | Regole di gioco |
| `ai/basic_ai.py` | Turno automatico P1 |

## Dipendenze runtime

- `fastapi`, `uvicorn`, `pydantic` (vedi `requirements.txt`)
- Nessun DB ancora (stato in RAM; una partita per processo)

## Prossimi passi

1. Deploy API su Render
2. Schema Supabase (partite persistenti / multiplayer)
3. Frontend Next.js più ricco (opzionale)
4. WebSocket per realtime

**Versione: v4**
