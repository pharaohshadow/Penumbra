# Roadmap Penumbra (aggiornata – v11)

## Stato attuale
**Completato: Fase 1 · Step 1.2 – Mostrissimi in UI**

Precedente: **1.1 Frammenti in UI** (v10)

### Cosa introduce v11
- Click su un Mostrissimo del pool → modalità sacrifici
- Click sulle tue creature per selezionare/deselezionare sacrifici
- Serve il numero richiesto; **almeno una su Cerchio Rituale** (caselle con ✧)
- **Conferma evocazione** → `POST /api/eldrazi`
- Board: flag `ritual` nelle celle; simbolo ✧

File in questa cartella (solo modificati):
- `api/main.py`
- `static/index.html`
- `ROADMAP.md`

---

## Cronologia

### Fase 0
- [x] v9 baseline online

### Fase 1 – Regole in partita
- [x] 1.1 Frammenti in UI (v10)
- [x] **1.2 Mostrissimi in UI (v11)** ← **sei qui**
- [ ] **1.3 Altare C3** ← prossimo
- [ ] 1.4 Effetti carte ondata 1
- [ ] 1.5 Mostro Neutrale attivo

### Fase 2 – Draft interattivo
- [ ] 2.1–2.3

### Fase 3 – Mappa / quest / snapshot
- [ ] 3.1–3.3

### Fase 4 – Multiplayer usabile
- [ ] 4.1–4.4

### Fase 5 – IA
- [ ] 5.1–5.3

### Fase 6 – Prodotto
- [ ] 6.1–6.5

---

## Deploy
Sovrascrivi in `/backend`:
- `api/main.py`
- `static/index.html`

Redeploy Render.
