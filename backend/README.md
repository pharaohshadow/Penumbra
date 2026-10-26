# Penumbra – Tactical Card Game 5×5 (v5)

Backend Python + IA + UI web, pronto per **Render**.

## Deploy su Render (test online)

### Opzione A – Blueprint (consigliata)
1. Su [render.com](https://render.com) → **New** → **Blueprint**
2. Collega il repo GitHub `Penumbra`
3. Se il file `render.yaml` è nella root del repo, Render lo legge da solo  
   Se `render.yaml` è dentro `backend/`, oppure imposta **Root Directory** = `backend`
4. Crea il servizio e attendi il deploy
5. Apri l’URL tipo: `https://penumbra-backend.onrender.com`

### Opzione B – Web Service manuale
1. **New** → **Web Service** → seleziona il repo
2. Impostazioni:
   - **Root Directory**: `backend`
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
3. Piano **Free** → Create Web Service

### Dopo il deploy
Apri l’URL di Render nel browser: vedrai la griglia e potrai giocare contro l’IA.

> Nota piano free: dopo ~15 min di inattività il servizio va in sleep; la prima richiesta successiva può richiedere 30–60 secondi.

## File di deploy

| File | Ruolo |
|------|--------|
| `requirements.txt` | Dipendenze Python |
| `Procfile` | Comando web (Heroku-style) |
| `runtime.txt` | Versione Python |
| `render.yaml` | Blueprint Render |
| `api/main.py` | FastAPI + CORS |
| `static/index.html` | UI giocabile |

## API

| Metodo | Path |
|--------|------|
| GET | `/` UI |
| GET | `/api/state` |
| POST | `/api/new` |
| POST | `/api/move` |
| POST | `/api/play` |
| POST | `/api/end` |

Vedi anche **`architettura.md`**.
