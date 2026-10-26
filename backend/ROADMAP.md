# Roadmap Penumbra (aggiornata – v10)

## Stato attuale
**Completato ora: Fase 1 · Step 1.1 – Frammenti in UI**

- API `POST /api/fragment` `{ game_id, coord, player_id }`
- UI: bottone **Piazza Corona** → click su tua creatura
- Status: frammenti rimanenti, costo prossimo (0/3/6), presenza Corona

Il resto dei file backend è ancora quello di **v9** (non duplicati in questa cartella).

---

## Cronologia

### Fase 0 – Baseline
- [x] v9 online (motore, IA, PvP, polling, portali, Supabase restore)

### Fase 1 – Regole che si sentono in partita
- [x] **1.1 Frammenti in UI** ← **sei qui (v10)**
- [ ] **1.2 Mostrissimi in UI** (prossimo)
- [ ] **1.3 Altare C3**
- [ ] **1.4 Effetti carte ondata 1**
- [ ] **1.5 Mostro Neutrale attivo**

### Fase 2 – Draft interattivo
- [ ] 2.1–2.3 Draft API + UI + passiva colori

### Fase 3 – Mappa / quest / snapshot
- [ ] 3.1–3.3 Eventi completi, Main Quest UI, snapshot tile

### Fase 4 – Multiplayer usabile
- [ ] 4.1–4.4 Realtime, lobby, auth, RLS

### Fase 5 – IA
- [ ] 5.1–5.3 Priorità GDD, difficoltà, log

### Fase 6 – Prodotto
- [ ] 6.1–6.5 Docs, tutorial, contenuti, CI

---

## Prossimo passo
**1.2 – Mostrissimi in UI**: selezionare dal pool, scegliere sacrifici (uno su Cerchio Rituale), conferma.

## Deploy v10
Copia solo questi file sopra la v9 su `/backend`:
- `api/main.py`
- `static/index.html`
Poi redeploy Render.
