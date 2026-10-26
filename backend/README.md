# Tactical Card Game 5×5 – Backend (v4)

Motore Python + **IA** + **UI web** (FastAPI + HTML).

## Come testare (browser)

```bash
cd backend
pip install -r requirements.txt
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Apri nel browser: **http://localhost:8000**

Vedrai la griglia 5×5, la mano, i comandi. L’IA gioca quando premi **Fine turno**.

### Controlli UI
- Clic su **tua unità** → clic su casella diagonale = muovi / attacca
- Clic su **carta Mostro** = evoca in zona Tempio
- Clic su **Trappola/Maledizione** → clic su casella target
- **Fine turno** = passa all’IA (gioca automaticamente)
- **Nuova partita** = reset

### CLI (opzionale)
```bash
python3 main.py
```

## Stack

| Layer | Tecnologia |
|-------|------------|
| Motore + IA | Python (`core/`, `ai/`) |
| API + UI | FastAPI + `static/index.html` |
| Docs Pages | `/docs` |
| Futuro | Supabase, Render, Next.js |

## API utili

| Metodo | Path | Descrizione |
|--------|------|-------------|
| GET | `/` | UI HTML |
| GET | `/api/state` | Stato partita |
| POST | `/api/new` | Nuova partita |
| POST | `/api/move` | `{from_coord, to_coord}` |
| POST | `/api/play` | `{hand_index, target_coord?}` |
| POST | `/api/eldrazi` | `{eldrazi_index, sacrifice_coords[]}` |
| POST | `/api/end` | Fine turno + turno IA |

Leggi **`architettura.md`** per la mappa del codice.
