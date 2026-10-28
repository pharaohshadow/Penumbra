# Penumbra – Consegna v28.2

## Cosa cambia

### Mappa 7×7 (da v28)
- Cornice non giocabile, zona interna 5×5
- Templi angoli: tu `A6`, IA `G0`
- Altare `D3`
- Spawn solo sul Tempio
- Muri = edge walls (linee tra celle)

### Hotfix errori
- **v28.1**: posizioni tempio hardcodate + messaggio errore chiaro su `/api/end`
- **v28.2**: implementato `_sync_fragment_card` mancante (causa del crash `AttributeError`)
- **v28.2**: muri ora visibili in UI come bordi grigi spessi tra le celle

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

1. Sostituisci i file dalla cartella `penumbra_v28`.
2. Ridistribuisci su Render.
3. Nuova partita base vs IA.
4. Controlla:
   - che non esca più l’errore su Fine turno
   - che i muri si vedano come linee grigie tra le celle
   - che templi/altare siano al posto giusto
