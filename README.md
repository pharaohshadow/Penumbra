# Penumbra – Consegna v27

Due cambiamenti UI / regole:

1. **Niente più pulsanti PvP / Unisciti** in partita (resta Partita base / vs IA dalla Home).
2. **Corona = carta in mano**, non più tasto «Piazza Corona».

**Nessuna modifica manuale richiesta.**

## Corona come carta

- In mano trovi **«Frammento / Corona»**
- Costo: **0** (primo), poi **3**, poi **6**
- Si gioca come le altre carte a bersaglio: click sulla carta → click su una tua creatura
- Dopo ogni piazzamento, se hai ancora frammenti, torna in mano con il costo successivo

## File da sostituire

| File | Azione |
|------|--------|
| `backend/core/game_state.py` | Sostituisci |
| `backend/static/index.html` | Sostituisci |
| `ROADMAP.md` | Sostituisci |
| `architettura.md` | Sostituisci |
| `istruzioni_per_IA.md` | Sostituisci |
| `README.md` | Questo handoff |
