# Penumbra – Consegna v28.3

## Cosa cambia

### Rimosso
- **Mostri Neutrali**: non spawnano più e non agiscono.

### Fog of War (nuova)
- Ogni giocatore vede solo le caselle entro **2 passi** (distanza Chebyshev / re degli scacchi) da:
  - una propria creatura, oppure
  - il proprio Tempio
- Caselle fuori nebbia: oscurate in UI (`░`), senza unità nemiche visibili
- **Magie di danno diretto** (maledizioni a bersaglio) **non possono** colpire creature nascoste dalla fog of war

### Già in v28–v28.2
- Mappa 7×7, templi angoli, muri edge, `_sync_fragment_card`, messaggio errore chiaro

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

1. Sostituisci i file e ridistribuisci su Render.
2. Nuova partita: verifica che non compaiano più neutrali e che la mappa sia oscurata lontano dalle tue creature/tempio.
3. Prova a bersagliare un nemico fuori visione con una maledizione → deve fallire con messaggio sulla nebbia.
