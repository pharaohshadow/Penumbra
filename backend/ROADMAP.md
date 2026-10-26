# Roadmap Penumbra (aggiornata – v13)

## Stato attuale
**Completato: Fase 1 · Step 1.4 – Effetti carte ondata 1**

### Cosa introduce v13
Solo `core/game_state.py`.

**Maledizioni (esempi):**
- Cure / Linfa / Raggio Solare → +1 HP alleato
- Benedizione Minore → +1 HP max
- Crescita Rigogliosa → +1/+1
- Preghiera → +1 mana
- Scudo di Fede → shield 2; Aegis → invulnerabile (fino a inizio tuo turno)
- Flash / Tocco Fossa → −1 ATK nemico
- Spark / Dardo / Giudizio / Succhiasangue / Drenaggio → danni (con lifesteal su succhia)
- Esecuzione → uccide nemico ≤2 HP
- Congelamento / Mente Confusa → stun
- Carica Frenetica → +1 ATK −1 HP
- Ondata di Furia → +1 ATK a tutti i tuoi
- Forza Gigantesca → +3 ATK e cura
- Richiamo Selvaggio → Lupo 2/1 in zona Tempio
- Fallback: 1 danno a nemico o cura 1 ad alleato se c’è target

**Trappole:** spine/fosse, mine, incendiaria ad area, mana steal, stun/liana, ecc.

**Stun:** blocca movimento; si rimuove a inizio turno del proprietario.

---

## Cronologia

### Fase 1
- [x] 1.1 Frammenti UI (v10)
- [x] 1.2 Mostrissimi UI (v11)
- [x] 1.3 Altare C3 (v12)
- [x] **1.4 Effetti carte ondata 1 (v13)** ← **sei qui**
- [ ] **1.5 Mostro Neutrale attivo** ← prossimo

### Fase 2–6
Invariate (draft, mappa, multiplayer, IA, prodotto).

---

## Deploy
Sovrascrivi:
- `backend/core/game_state.py`

Redeploy Render.
