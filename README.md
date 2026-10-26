# Penumbra – Consegna v25 (step 5.4 – primi fix regole)

Correzioni automatiche trovate nel motore di gioco (senza elenco da parte tua).

**Nessuna modifica manuale richiesta.**

## Cosa è stato sistemato

1. **Malattia da evocazione**  
   Le creature appena evocate non dovevano attaccare subito (salvo parole chiave speciali).  
   Ora la limitazione vale davvero e **scade all’inizio del turno successivo**.

2. **Fuoco amico**  
   Non si può più “attaccare” (muovere su) una creatura **alleata**.

3. **Attacco nel turno sbagliato**  
   Se una creatura non può attaccare in questo turno, non può entrare in combattimento.

## File da sostituire

| File | Azione |
|------|--------|
| `backend/core/game_state.py` | Sostituisci |
| `ROADMAP.md` | Sostituisci |
| `architettura.md` | Sostituisci |
| `istruzioni_per_IA.md` | Sostituisci |
| `README.md` | Questo handoff |

## Ancora utile da te

Se noti altre regole sbagliate (carte, draft, corona, mana, vittoria…), elencale e le sistemiamo nel prossimo giro.
