# ARCHITETTURA – Penumbra v5

Documento di riferimento completo.

---

## 1. Visione

Card game tattico a turni, ambientazione egizia.  
Ispirazioni: Mage Wars Arena + Yu-Gi-Oh Duel Links.

Partita base = VS IA. Modalità future = modificatori.

---

## 2. Regole complete

### Griglia
- 4×5, movimento 1 passo ortogonale, niente sovrapposizione

### Magus
- 20 HP, 1 ATK

### Azioni per turno
- Ogni unità mobile fa **una sola azione** (muovere **oppure** attaccare)
- Le **Torri non agiscono** (non si selezionano per muovere/attaccare)

### Combattimento
- Solo melee
- Danno = ATK base + bonus aura dalle Torri alleate adiacenti

### Powa
- Turno 1: 1 Powa
- All’inizio del turno: +Powa = numero turno (max 6)
- Non si perde

### Mano
- 10 carte dall’inizio (8 Creature + 2 Torri)
- Non si pesca

### Evocazione
- Creature e Torri: costo Powa, casella vuota adiacente al Magus
- Appena evocate hanno `acted = true`

### Torri
- `type: 'tower'`, `atk: 0`
- Non si muovono
- Possono essere attaccate e distrutte
- Passive attuale: `aura_atk` → alleati adiacenti +1 ATK (valore in `passiveValue`)

### Vittoria
- Solo Magus avversario a 0 HP

---

## 3. Tipi di carte

| Tipo        | Stato v5      | Note                                      |
|-------------|---------------|-------------------------------------------|
| Creature    | ✅            | ATK + HP, si muovono e attaccano          |
| Torri       | ✅            | Solo HP + aura, non si muovono            |
| Armi        | ❌ Futuro     | Equipaggiamento, occupano “mani”          |
| Maledizioni | ❌ Futuro     | Solo nel proprio turno, “in aria”         |
| Trappole    | ❌ Futuro     | Solo nel turno avversario, “in aria”      |

---

## 4. Architettura tecnica

```
docs/
├── index.html
├── css/style.css
└── js/
    ├── cards.js
    ├── engine.js
    └── ui.js
```

- `getEffectiveAtk(r,c)` calcola ATK + aura delle torri adiacenti
- `summonCard` gestisce sia creature che torri

### Stack
- Frontend: GitHub Pages (`docs/`)
- Futuro: Supabase, Render

---

## 5. Cosa funziona in v5

- Tutto della v4
- Torri evocabili (Obelisco, Pilastro)
- Aura +ATK agli alleati adiacenti
- IA evoca e usa le torri
- UI distingue carte torre e unità torre

---

## 6. Prossimi passi (v6)

1. Armi (equip su creature con mani libere)
2. Maledizioni / Trappole base
3. Bilanciamento costi e stats
4. Animazioni danno / evocazione

---

## 7. Note per lo sviluppatore

- Utente non tecnico → file pronti, istruzioni chiare
- Ogni consegna = cartella `vN` con README + ARCHITETTURA + file
- Rileggere sempre engine.js / ui.js prima di modifiche

---

**Versione:** v5  
**Data:** 24 ottobre 2026  
**Stato:** Torri + aura +ATK funzionanti  
