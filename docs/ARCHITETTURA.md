# ARCHITETTURA – Penumbra v8

Documento di riferimento completo.

---

## 1. Visione

Card game tattico a turni, ambientazione egizia.  
Partita base = VS IA. Grafica e feedback stile Duel Links.

---

## 2. Regole

Come v7 (Creature, Torri, Armi, Maledizioni, Trappole, griglia 4×5, Powa, melee).

---

## 3. Animazioni (v8)

Implementate solo in **UI** (CSS + `ui.js`), senza cambiare le regole.

| Evento           | Effetto                                      |
|------------------|----------------------------------------------|
| Evocazione / move| `anim-summon` (scale pop)                    |
| Attacco          | `anim-attack` sull’attaccante                |
| Danno subito     | `anim-shake` + numero flottante `−N`         |
| Casella colpita  | `anim-flash`                                 |
| Trappola posata / scattata | flash sul badge 🪤                  |
| Equip arma       | pulse sull’unità                             |

Metodi UI:
- `animUnit(r, c, className)`
- `animCell(r, c)`
- `showDamage(r, c, amount, kind?)`
- `animTrapBadge()`
- `animHpBar(who)`

---

## 4. Struttura file

```
docs/
├── index.html
├── css/style.css   ← keyframes + classi anim-*
└── js/
    ├── cards.js
    ├── engine.js   ← invariato rispetto a v7
    └── ui.js       ← helper animazioni + chiamate dopo le azioni
```

---

## 5. Prossimi passi

1. Bilanciamento / più carte
2. Modalità (Endless, Storia, PvP)
3. Suoni
4. Supabase (utenti / mazzi)

---

**Versione:** v8  
**Data:** 24 ottobre 2026  
**Stato:** Animazioni di combattimento e evocazione attive  
