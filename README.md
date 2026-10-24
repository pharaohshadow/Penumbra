# Penumbra

**Gioco di carte tattico egizio su griglia**  
Partite veloci (~5 minuti) – Browser – Grafica stile Yu-Gi-Oh Duel Links

---

## Cos’è Penumbra

Penumbra è un gioco di carte a turni ambientato nell’antico Egitto.  
Si gioca su una **griglia 4×5**.  
Il movimento e il posizionamento sono fondamentali.

L’obiettivo è **ridurre a 0 i punti vita** del Magus avversario.

---

## Stato attuale – v5

**Novità: Torri!**

- Puoi evocare **Torri** (Obelisco Guardiano, Pilastro del Nilo)
- Le Torri **non si muovono** e non attaccano
- Hanno tanti HP e danno **+1 ATK** a tutti gli alleati adiacenti
- In mano vedi 8 Creature + 2 Torri
- L’IA usa anche le Torri

| Azione     | Colore  | Cosa fa                                      |
|------------|---------|----------------------------------------------|
| Movimento  | Giallo  | 1 passo ortogonale                           |
| Attacco    | Rosso   | Danni in melee (include bonus dalle Torri)   |
| Evocazione | Verde   | Piazza Creatura o Torre accanto al Magus     |

---

## Regole rapide

- Ogni unità (tranne le Torri) fa **una sola azione per turno**
- Creature appena evocate non agiscono nello stesso turno
- Torri: solo HP + aura +ATK, si possono attaccare e distruggere
- Vittoria = Magus avversario a 0 HP

---

## Struttura file (v5)

```
docs/
├── index.html
├── ARCHITETTURA.md
├── css/style.css
└── js/
    ├── cards.js    ← Creature + Torri
    ├── engine.js
    └── ui.js
```

---

## Roadmap

- v1 Documentazione → FATTA  
- v2 Griglia + movimento → FATTA  
- v3 Attacco melee → FATTA  
- v4 Mano + Creature → FATTA  
- v5 Torri + aura → FATTA  
- **v6** (prossima) Armi / Maledizioni / bilanciamento  

---

## Come caricare su GitHub

| File locale                     | Dove metterlo                |
|---------------------------------|------------------------------|
| `v5/README.md`                  | → root (`README.md`)         |
| `v5/docs/ARCHITETTURA.md`       | → `docs/ARCHITETTURA.md`     |
| `v5/docs/index.html`            | → `docs/index.html`          |
| `v5/docs/css/style.css`         | → `docs/css/style.css`       |
| `v5/docs/js/cards.js`           | → `docs/js/cards.js`         |
| `v5/docs/js/engine.js`          | → `docs/js/engine.js`        |
| `v5/docs/js/ui.js`              | → `docs/js/ui.js`            |

**https://pharaohshadow.github.io/Penumbra/**

---

**Versione:** v5 – Torri + aura +ATK  
**Data:** 24 ottobre 2026  
