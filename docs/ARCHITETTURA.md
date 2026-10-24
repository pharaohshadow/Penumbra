# ARCHITETTURA – Penumbra v9

Documento di riferimento completo.

---

## 1. Visione

Card game tattico a turni, ambientazione egizia.  
Partita base = VS IA.

---

## 2. Regole e gameplay

Come v7/v8 (Creature, Torri, Armi, Maledizioni, Trappole, animazioni).

---

## 3. Layout visualizzazione (v9)

### Struttura HTML

```
.page-shell
  ├── .side-panel.side-left   (solo PC)
  ├── #app.game-column        (il gioco)
  └── .side-panel.side-right  (solo PC)
```

### Comportamento

| Viewport | Comportamento |
|----------|----------------|
| **&lt; 768px** (mobile) | Solo `#app`, larghezza 100%, altezza 100dvh, safe-area |
| **≥ 768px** (PC) | 3 colonne: laterali flessibili + centro fisso ~420px |
| **≥ 1100px** | Centro ~440px |

La colonna centrale su PC è **identica** all’esperienza mobile: stesso UI, stessa griglia, stessa mano.

### CSS chiave

- `100dvh` per altezza viewport moderna
- `env(safe-area-inset-*)` per notch / home bar
- `.side-panel { display: none }` di default, `display: block` da 768px

---

## 4. Struttura file

```
docs/
├── index.html      ← page-shell + side panels
├── css/style.css   ← layout 3 colonne
└── js/             ← invariato rispetto a v8
```

---

## 5. Prossimi passi

1. Bilanciamento / più carte  
2. Modalità (Endless, Storia, PvP)  
3. Suoni  
4. Supabase  

---

**Versione:** v9  
**Data:** 24 ottobre 2026  
**Stato:** Layout mobile full-screen + PC a 3 colonne  
