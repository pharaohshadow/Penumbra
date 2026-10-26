# Architettura – Penumbra v5

## Repo

```
Penumbra/
├── backend/          # codice gioco + API
│   ├── api/main.py
│   ├── static/index.html
│   ├── core/
│   ├── ai/
│   ├── requirements.txt
│   ├── Procfile
│   ├── runtime.txt
│   ├── render.yaml
│   ├── README.md
│   └── architettura.md
└── docs/             # GitHub Pages (solo documentazione)
```

## Deploy

- **Host**: Render (Web Service)
- **Root Directory**: `backend`
- **Start**: `uvicorn api.main:app --host 0.0.0.0 --port $PORT`
- Stato partita: **in memoria** (una sessione per istanza; si resetta al restart/sleep)

## Flusso online

1. Browser → URL Render
2. `GET /` serve `static/index.html`
3. JS parla con `/api/*` sullo stesso origin
4. `POST /api/end` esegue il turno IA sul server

## Prossimi passi

1. Supabase: salvare partite / utenti (opzionale multiplayer)
2. WebSocket se serve realtime tra due umani
3. Frontend Next.js separato (solo se serve SEO/UI più ricca)

**Versione: v5**
