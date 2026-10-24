# ARCHITETTURA – Penumbra v7

Documento di riferimento completo.

---

## 1. Visione

Card game tattico a turni, ambientazione egizia. Partita base = VS IA.

---

## 2. Regole complete

### Griglia / Magus / Powa / Movimento / Combattimento
- Come v6 (4×5, 20 HP Magus, Powa max 6, melee, 1 azione/turno)

### Tipi di carte (tutti implementati)

| Tipo        | Quando          | Come                                      |
|-------------|-----------------|-------------------------------------------|
| Creature    | Tuo turno       | Evoca su casella adiacente al Magus       |
| Torri       | Tuo turno       | Evoca; immobile; aura +ATK                |
| Armi        | Tuo turno       | Equip su unità con mani libere            |
| Maledizioni | **Solo tuo turno** | Target nemico → danno immediato        |
| Trappole    | Si posano nel tuo turno | Scattano quando un **nemico attacca** |

### Maledizione
- Costo Powa, scegli un nemico sulla griglia
- Infligge `damage` HP
- “In aria” (non resta sulla griglia)

### Trappola
- Costo Powa, si posa senza target (`traps.player[]` / `traps.ai[]`)
- Alla prima volta che un’unità **avversaria attacca**, la trappola scatta:
  - danno all’attaccante
  - trappola consumata
- Visibile come contatore 🪤

### Vittoria
- Magus avversario a 0 HP

---

## 3. Architettura

```
docs/js/
├── cards.js
├── engine.js   ← castCurse, setTrap, triggerTrap
└── ui.js
```

---

## 4. Cosa funziona in v7

- Tutti i 5 tipi di carte
- Maledizione con target viola
- Trappole posate + trigger automatico in attacco
- IA usa curse/trap/equip/summon
- Badge trappole in UI

---

## 5. Prossimi passi (v8+)

1. Bilanciamento numeri e costi
2. Più carte per tipo
3. Animazioni / feedback visivo
4. Modalità (Endless, Storia, PvP)
5. Supabase (utenti / mazzi)

---

**Versione:** v7  
**Data:** 24 ottobre 2026  
**Stato:** Maledizioni + Trappole funzionanti – set carte completo  
