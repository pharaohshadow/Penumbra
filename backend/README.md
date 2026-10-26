# Penumbra – Tactical Card Game 5×5 (v8)

## Novità v8
- **Polling UI** ogni 2.5s quando non è il tuo turno (PvP si aggiorna da solo)
- **Portali**: entrando in un portale vieni teletrasportato su una casella libera adiacente al portale collegato (Bianco↔Nero)

## Online
Redeploy su Render, apri l’URL.

- **Nuova vs IA** / **Nuova PvP** / **Unisciti** come in v7
- In PvP il guest vede le mosse dell’host senza ricaricare la pagina

## Deploy
Root `backend` · `pip install -r requirements.txt` · `uvicorn api.main:app --host 0.0.0.0 --port $PORT`

Vedi **architettura.md**.
