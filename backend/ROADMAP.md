# Roadmap Penumbra (aggiornata – v12)

## Stato attuale
**Completato: Fase 1 · Step 1.3 – Altare C3 (Evoluzione)**

### Cosa introduce v12
- Se una tua creatura **inizia il turno** su **C3 (Altare)**:
  - prima volta: status `evolved`, **+1 ATK permanente**, **+1 HP**
  - turni successivi sull’Altare: solo **+1 HP**
- UI: ✦ sull’unità evoluta; casella vuota mostra **✦Altare**
- API: `unit.evolved`, `cell.altar`

File modificati in questa cartella:
- `core/game_state.py`
- `api/main.py`
- `static/index.html`
- `ROADMAP.md`

---

## Cronologia

### Fase 0
- [x] v9 baseline

### Fase 1 – Regole in partita
- [x] 1.1 Frammenti UI (v10)
- [x] 1.2 Mostrissimi UI (v11)
- [x] **1.3 Altare C3 (v12)** ← **sei qui**
- [ ] **1.4 Effetti carte ondata 1** ← prossimo
- [ ] 1.5 Mostro Neutrale attivo

### Fase 2 – Draft
- [ ] 2.1–2.3

### Fase 3 – Mappa / quest
- [ ] 3.1–3.3

### Fase 4 – Multiplayer
- [ ] 4.1–4.4

### Fase 5 – IA
- [ ] 5.1–5.3

### Fase 6 – Prodotto
- [ ] 6.1–6.5

---

## Deploy
Sovrascrivi in `/backend` i tre path sopra, poi redeploy Render.

## Come testare
Muovi un’unità su C3, **Fine turno** fino a quando è di nuovo il tuo turno con quella unità ancora su C3 → log “Altare C3: … evolve” e ATK+1.
