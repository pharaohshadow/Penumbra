# ARCHITETTURA – Penumbra v4

Documento di riferimento completo.  
Leggendo questo file + il README si può riprendere il lavoro da zero.

---

## 1. Visione

Card game tattico a turni, ambientazione egizia.  
Ispirazioni: Mage Wars Arena (griglia + mano completa) + Yu-Gi-Oh Duel Links (grafica).

Partita base = VS IA.  
Modalità future = modificatori della partita base.

---

## 2. Regole complete

### Griglia
- 4×5, movimento 1 passo ortogonale, niente sovrapposizione

### Magus
- 20 HP, 1 ATK, sempre sulla griglia

### Azioni per turno
- Ogni unità può fare **una sola azione** (muovere **oppure** attaccare)
- Flag `acted`

### Combattimento
- Solo melee (adiacente ortogonale)
- Danno = ATK → a 0 HP l’unità va nel Cimitero

### Powa
- Inizio turno 1: 1 Powa ciascuno
- All’inizio del proprio turno: +Powa pari al numero del turno (max 6)
- Non si perde mai

### Mano
- 10 carte dall’inizio, **non si pesca**
- Stesso mazzo base per player e IA (per ora)

### Evocazione Creature
- Costo in Powa
- Solo su casella **vuota adiacente al proprio Magus**
- La Creatura evocata ha `acted = true` (non agisce nello stesso turno)

### Vittoria
- Solo Magus avversario a 0 HP

---

## 3. Tipi di carte (implementati / previsti)

| Tipo        | Stato v4      | Note                                      |
|-------------|---------------|-------------------------------------------|
| Creature    | ✅ Implementato | ATK + HP, si muovono e attaccano          |
| Torri       | ❌ Futuro     | Solo HP + abilità passive, non si muovono |
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
    ├── cards.js    ← pool carte + createStartingHand()
    ├── engine.js   ← stato e regole pure
    └── ui.js       ← DOM e input
```

- **engine.js** non tocca il DOM
- **ui.js** legge `Game.getState()` e chiama metodi del Game

### Stack
- Frontend: GitHub Pages (`docs/`)
- Futuro: Supabase (utenti + carte), Render (se serve backend)

---

## 5. Cosa funziona in v4

- Griglia, movimento, attacco melee
- Mano di 10 carte visualizzata
- Selezione carta → evidenziazione caselle verdi
- Evocazione Creature pagando Powa
- Creature con ATK/HP diversi, si muovono e attaccano
- IA che evoca creature e combatte con tutte le sue unità
- Vittoria/sconfitta + Rigioca
- Un’azione per unità per turno

---

## 6. Prossimi passi (v5)

1. Torri (immobili, solo HP + passiva semplice)
2. Armi (equipaggiamento che aumenta ATK)
3. Maledizioni / Trappole base
4. Bilanciamento numeri e costi
5. Feedback visivo più ricco (animazioni danno, evocazione)

---

## 7. Note per lo sviluppatore

- L’utente non è tecnico → file pronti da caricare, istruzioni chiare
- Ogni consegna = cartella `vN` con README + ARCHITETTURA + tutti i file
- Prima di modificare `engine.js` / `ui.js` rileggerli sempre

---

**Versione:** v4  
**Data:** 24 ottobre 2026  
**Stato:** Mano + evocazione Creature funzionanti  
