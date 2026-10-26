# Tactical Card Game 5×5 – Backend (v3)

Motore di gioco Python puro + **IA base**.

## Cosa c’è in v3

Tutto di v2 **più**:

- **IA base** (`ai/basic_ai.py`) che controlla il giocatore in alto (P1)
- Priorità IA:
  1. Piazza Frammento se manca
  2. Gioca carte economiche (Mostri / Maledizioni / Trappole)
  3. Attacca Corona nemica o unità adiacenti
  4. Muove verso Altare / Corona
  5. Tenta Mostrissimo se ha abbastanza sacrifici + Cerchio Rituale
  6. Fine turno
- CLI: quando è il turno dell’IA, gioca automaticamente

## Come testare

```bash
cd backend
python3 main.py
```

L’IA gioca da sola quando è il suo turno. Tu comandi solo il giocatore in basso.

### Comandi CLI (umano)

| Comando | Descrizione |
|---------|-------------|
| `m B5 C4` | Muovi unità |
| `p 0` / `p 2 B5` | Gioca carta dalla mano |
| `x 0 A1 B5` | Evoca Mostrissimo (sacrifici) |
| `s` | Stato |
| `e` | Fine turno (passa all’IA) |
| `q` | Esci |

## Stack

| Layer | Tecnologia |
|-------|------------|
| Logica + IA | Python 3.12 |
| API | FastAPI (prossimo) |
| Frontend | Next.js |
| DB / Auth / Realtime | Supabase |
| Hosting | Render |
| Docs (Pages) | `/docs` |

## Prossimi passi (v4+)

1. FastAPI + WebSocket (stato partita, mosse)
2. Schema Supabase
3. Frontend griglia
4. Deploy Render

Leggi **`architettura.md`** per la mappa completa del codice.
