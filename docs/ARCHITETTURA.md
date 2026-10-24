# ARCHITETTURA – Penumbra v6

Documento di riferimento completo.

---

## 1. Visione

Card game tattico a turni, ambientazione egizia.  
Partita base = VS IA.

---

## 2. Regole complete

### Griglia
- 4×5, movimento 1 passo ortogonale

### Magus
- 20 HP, 1 ATK, **2 mani**

### Azioni
- Un’azione per unità mobile per turno (muovere **oppure** attaccare)
- Torri non agiscono

### Combattimento
- Melee only
- Danno = ATK base + **armi equipaggiate** + **aura torri adiacenti**

### Powa
- Turno 1: 1 | Guadagno = numero turno (max 6) | Non si perde

### Mano
- 10 carte (6 Creature + 2 Torri + 2 Armi), non si pesca

### Evocazione (Creature / Torri)
- Casella vuota adiacente al Magus

### Armi
- type: `weapon`
- `atkBonus`, `handsRequired`
- Si equipaggiano su unità alleate (creature o Magus) con mani libere sufficienti
- Non finiscono sulla griglia: si attaccano all’unità (`unit.weapons[]`)
- Quando l’unità muore, le armi vanno perse (nel cimitero con l’unità)

### Torri
- Immobili, aura `aura_atk` (+1 ATK agli alleati adiacenti)

### Vittoria
- Magus avversario a 0 HP

---

## 3. Tipi di carte

| Tipo        | Stato | Note                                      |
|-------------|-------|-------------------------------------------|
| Creature    | ✅    | ATK + HP + mani                           |
| Torri       | ✅    | Solo HP + aura                            |
| Armi        | ✅    | Equip, +ATK, richiedono mani              |
| Maledizioni | ❌    | Futuro – solo nel proprio turno           |
| Trappole    | ❌    | Futuro – solo nel turno avversario        |

---

## 4. Architettura

```
docs/js/
├── cards.js    ← pool carte
├── engine.js   ← logica (equipWeapon, getWeaponAtkBonus, getFreeHands)
└── ui.js       ← evidenziazione blu per equip
```

---

## 5. Cosa funziona in v6

- Tutto delle v precedenti
- Armi giocabili e equipaggiabili
- Mani libere / usate
- ATK effettivo = base + armi + aura
- IA equipaggia armi e combatte
- UI: caselle blu, icone arma sulle unità

---

## 6. Prossimi passi (v7)

1. Maledizioni / Trappole
2. Bilanciamento
3. Animazioni
4. (Opzionale) Supabase per salvare mazzi

---

**Versione:** v6  
**Data:** 24 ottobre 2026  
**Stato:** Armi equipaggiabili funzionanti  
