# Penumbra – Consegna v28.1 (hotfix)

## Cosa cambia (rispetto a v27)

1. **Mappa 7×7**
   - Cornice esterna non giocabile
   - Zona interna 5×5 giocabile
   - Templi agli **angoli**:
     - Tempio 1 (tu) = basso-sinistra `A6`
     - Tempio 2 (IA) = alto-destra `G0`
   - Spawn creature **solo** sulla casella del Tempio
   - Altare al centro della zona giocabile `D3`

2. **Muri non sono più celle**
   - Diventano **linee tra le caselle** (edge walls)
   - Layout = bordi blu del tuo map.xlsx
   - Le creature non possono attraversarli

3. Coordinate nuove: **A–G / 0–6**

4. **Hotfix 500 su /api/end**
   - Corrette posizioni tempio ancora hardcodate a 5×5 in evocazione mostri
   - `/api/end` ora restituisce il messaggio di errore reale invece di un 500 generico

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

1. Sostituisci i file (cartella `penumbra_v28` negli artifacts).
2. Riavvia / ridistribuisci su Render.
3. Fai una **nuova partita base vs IA**.
4. Se esce ancora errore, copia il **testo completo** del messaggio (ora sarà leggibile, es. `Errore fine turno: ...`) e incollamelo.
