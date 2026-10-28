# Penumbra – Consegna v30

## Neutrali colorati (Altare)
- A fine turno di ogni giocatore: attivazione + spawn sull’Altare
- **Stats**: `atk = floor(media_atk di TUTTI i mostri giocatori) − 1` (min 0), `hp = floor(media_hp)` (min 1) → minimo **0/1**
- **Colore** casuale tra i non ancora usciti nel ciclo: Bianco, Blu, Rosso, Nero, Verde, **Giallo**
- Dopo i 6 colori → **Il Signore**; poi il ciclo colori si azzera

## Il Signore
- Spawna su **casella casuale** libera (non sull’Altare)
- Sulla stessa casella lascia un **artefatto** (◆)
- Stats: **ATK = 0, +2 a ogni comparsa successiva**; **HP = infinito**
- Non bersagliabile, non attaccabile
- Vaga a caso a fine turno; interazione se condivide/adiacenza con un giocatore (log per ora)

## Artefatto e indizi
- Entrando sulla casella dell’artefatto, la creatura del giocatore lo raccoglie
- +1 indizio + **popup “GGWP”** (placeholder testo indizio)
- Contatore indizi in status bar

**Nessuna modifica manuale richiesta.**

Cartella: `penumbra_v30/`

### File principali
| File | Azione |
|------|--------|
| `backend/core/game_state.py` | Sostituisci |
| `backend/core/player.py` | Sostituisci |
| `backend/core/tile.py` | Sostituisci |
| `backend/api/main.py` | Sostituisci |
| `backend/static/index.html` | Sostituisci |
| docs | Sostituisci |
