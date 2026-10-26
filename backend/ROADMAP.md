# Roadmap Penumbra (aggiornata – v19)

## Stato attuale
**Completato: Fase 3 · Step 3.2 – Main Quest UI**

### Cosa introduce v19
- API: `quest_progress` con label, regole e avanzamento per giocatore
- UI: pannello **★ Main Quest**
  - se assente: invito a esplorare
  - **Dominio**: Buff x/2 + Altare sì/no
  - **Superiorità**: unità vs avversario (+3)

File: `api/main.py`, `static/index.html`

---

## Cronologia

### Fase 3
- [x] 3.1 Tessere evento (v18)
- [x] **3.2 Main Quest UI (v19)** ← **sei qui**
- [ ] **3.3 Snapshot tile ricco** ← prossimo

### Fase 4–6
Invariate

---

## Deploy
Sovrascrivi in `/backend` i due file, redeploy.
