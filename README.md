# Penumbra – Consegna v28

## Cosa cambia

1. **Mappa 7×7**
   - Cornice esterna non giocabile
   - Zona interna 5×5 giocabile
   - Templi agli **angoli**:
     - Tempio 1 (tu) = basso-sinistra
     - Tempio 2 (IA) = alto-destra
   - Spawn creature **solo** sulla casella del Tempio
   - Altare al centro della zona giocabile

2. **Muri non sono più celle**
   - Diventano **linee tra le caselle** (edge walls)
   - Layout = esattamente i bordi blu del tuo file map.xlsx
   - Le creature non possono attraversarli

3. Coordinate nuove: **A–G / 0–6**

**Nessuna modifica manuale richiesta.**

---

## File da sostituire

| File | Azione |
|------|--------|
| `backend/core/constants.py` | Sostituisci |
| `backend/core/map_board.py` | Sostituisci |
| `backend/core/tile.py` | Sostituisci |
| `backend/core/game_state.py` | Sostituisci |
| `backend/api/main.py` | Sostituisci |
| `backend/static/index.html` | Sostituisci |
| `ROADMAP.md` | Sostituisci |
| `architettura.md` | Sostituisci |
| `istruzioni_per_IA.md` | Sostituisci |
| `README.md` | Questo handoff |

---

## Cosa fare dopo

1. Sostituisci i file elencati sopra.
2. Riavvia / ridistribuisci il backend.
3. Fai una **nuova partita base vs IA**.
4. Dimmi se l’errore del 3° turno si ripresenta o se la mappa ti torna corretta (templi, muri, altare, spawn).
