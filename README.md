# Penumbra – Tactical Card Game 5×5

**Consegna v1** (step 3.3 – Snapshot tile ricco)

Questo file è il **punto di ingresso unico** per un passaggio di consegne a una nuova chat.
Copia/incolla (o allega) questo README + i file nella cartella `v1/` alla nuova conversazione.

## Cosa contiene questa cartella `v1/`

| File | Ruolo |
|------|--------|
| `README.md` (questo) | Handoff + indice |
| `architettura.md` | Architettura aggiornata (restore + snapshot tile) |
| `ROADMAP.md` | Roadmap aggiornata – dove siamo arrivati |
| `istruzioni_per_IA.md` | Preferenze e istruzioni operative dell’autore |
| `backend/api/main.py` | `serialize_state` arricchito (campi tile) + version 0.20 |
| `backend/api/restore.py` | `hydrate` che ripristina i tile dallo snapshot |

## Cosa è stato fatto in v1

- **Step 3.3 completato**: snapshot board più ricco.
- In `serialize_state` ogni cella board salva anche:
  - `permanent_effect`
  - `trap_card_id`
  - `wall_hp`
  - `owner_id`
- In `hydrate` questi campi vengono applicati al `Tile` dopo il layout fisso del costruttore.
- **Backward compatible**: snapshot vecchi (senza i nuovi campi) continuano a funzionare.
- Nessuna modifica alla logica di gioco, AI, draft, quest, UI.

## Come applicare su GitHub / Render

1. Sovrascrivi nel repo:
   - `backend/api/main.py`
   - `backend/api/restore.py`
2. (Opzionale ma consigliato) aggiorna anche i doc in root backend:
   - `backend/README.md` ← puoi usare questo README come base
   - `backend/architettura.md`
   - `backend/ROADMAP.md`
3. Redeploy su Render.

## Prossimo step (vedi ROADMAP)

Dopo 3.3: definire/proseguire Fase 4 (o eventuali micro-fixi ancora in Fase 3, es. status temporanei unità nello snapshot).

## Link repo

https://github.com/pharaohshadow/Penumbra
