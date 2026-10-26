# Roadmap Penumbra (aggiornata – v20)

## Stato attuale

**Completato: Fase 3 · Step 3.3 – Snapshot tile ricco** ← **sei qui (consegna v1)**

### Cosa introduce v20 (questa consegna)

- `serialize_state`: board cell con `permanent_effect`, `trap_card_id`, `wall_hp`, `owner_id`
- `hydrate`: applica i campi tile dallo snapshot (compatibile con snapshot pre-v20)
- Nessun breaking change su API pubbliche o UI

File modificati in questa consegna:
- `backend/api/main.py`
- `backend/api/restore.py`

---

## Cronologia

### Fase 3

- [x] 3.1 Tessere evento (v18)
- [x] 3.2 Main Quest UI (v19)
- [x] **3.3 Snapshot tile ricco (v20)** ← **fatto in v1**

### Possibili micro-step residuali Fase 3 (non bloccanti)

- [ ] 3.4 Snapshot status temporanei unità
- [ ] 3.5 Restore draft completo (opzionale)

### Fase 4–6

Invariate rispetto al piano precedente (da dettagliare quando si chiude Fase 3):

- Realtime / multiplayer più solido
- Auth
- Frontend più ricco / polish
- Bilanciamento e contenuto carte

---

## Deploy

Sovrascrivi in `/backend` i file di questa cartella `v1/backend/…`, poi redeploy Render.
