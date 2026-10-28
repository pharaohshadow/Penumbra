# Penumbra – Consegna v29

## Novità

### Cartelle versione
Da questa consegna in poi ogni handoff è in `penumbra_vXX` ascendente (regola scritta in `istruzioni_per_IA.md`).

### Neutrali dall’Altare
A **fine turno di ogni giocatore**:
1. Si attivano i neutrali già in campo
2. Spawna sull’**Altare** una nuova creatura neutrale

**Progressione stats**
| Spawn | Stats | Nome |
|-------|-------|------|
| 1° | 1/1 | Neutrale 1/1 |
| 2° | 2/2 | Neutrale 2/2 |
| … | … | … |
| 6° | 6/6 | **Il Signore** |
| 7° | 1/1 | (ciclo riparte) |

**Comportamento (non-Signore)**
1. **Senza bersaglio**: fa 1 passo in direzione casuale; se nella sua fog (raggio 2) vede creature giocatore, ne sceglie una a caso come bersaglio.
2. **Con bersaglio**: fa 1 passo verso di lui; se può entrare sulla sua casella → combattimento.

**Il Signore (6/6)**  
BBEG. Per ora compare e non usa ancora le regole speciali (in attesa tue istruzioni).

### Già presente (v28.x)
- Mappa 7×7, muri edge, fog of war, Corona carta, no PvP in partita

**Nessuna modifica manuale richiesta.**

---

## File da sostituire

| File | Azione |
|------|--------|
| `backend/core/game_state.py` | Sostituisci |
| `backend/core/constants.py` | Sostituisci (se non già v28) |
| `backend/core/map_board.py` | Sostituisci (se non già v28) |
| `backend/core/tile.py` | Sostituisci (se non già v28) |
| `backend/api/main.py` | Sostituisci (se non già v28) |
| `backend/static/index.html` | Sostituisci (se non già v28) |
| `ROADMAP.md` | Sostituisci |
| `architettura.md` | Sostituisci |
| `istruzioni_per_IA.md` | Sostituisci |
| `README.md` | Questo handoff |

Cartella: `/home/workdir/artifacts/penumbra_v29/`

---

## Prossimo
- Tu mi spieghi le regole del **Signore**
- Io le implemento in **v30**
