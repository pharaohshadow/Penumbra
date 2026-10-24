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

## Stato attuale – v4

**Ora puoi giocare le carte!**

Cosa puoi fare:
- Vedi la **mano di 10 carte** in basso
- Clicca una carta (se hai abbastanza Powa) → caselle **verdi** = dove puoi evocarla
- Evoca Creature accanto al tuo Magus
- Le Creature possono muovere e attaccare (dal turno successivo)
- L’IA evoca anche lei e combatte con le sue creature
- Movimento (giallo), Attacco (rosso), Evocazione (verde)

---

## Regole rapide

| Azione        | Colore casella | Cosa fa                          |
|---------------|----------------|----------------------------------|
| Movimento     | Giallo         | Sposta di 1 passo ortogonale     |
| Attacco       | Rosso          | Infligge ATK danni in melee      |
| Evocazione    | Verde          | Piazza una Creatura (costa Powa) |

- Ogni unità fa **una sola azione per turno**
- Le Creature appena evocate non agiscono nello stesso turno
- Si evoca **solo** su caselle adiacenti al proprio Magus
- Vittoria = Magus avversario a 0 HP

---

## Stack tecnico

| Parte       | Tecnologia     |
|-------------|----------------|
| Frontend    | HTML + CSS + JS (GitHub Pages su `docs/`) |
| Carte/Utenti| Supabase (prossimamente) |
| Backend     | Render (solo se servirà) |

---

## Struttura file (v4)

```
docs/
├── index.html
├── ARCHITETTURA.md
├── css/style.css
└── js/
    ├── cards.js    ← definizione delle 10 carte
    ├── engine.js   ← logica di gioco
    └── ui.js       ← interfaccia
```

---

## Roadmap

- **v1** Documentazione → FATTA  
- **v2** Griglia + movimento → FATTA  
- **v3** Attacco melee → FATTA  
- **v4** Mano + Creature → FATTA  
- **v5** (prossima) Torri / Armi / Maledizioni / bilanciamento  

---

## Come caricare su GitHub

| File locale                     | Dove metterlo sul repository |
|---------------------------------|------------------------------|
| `v4/README.md`                  | → root (`README.md`)         |
| `v4/docs/ARCHITETTURA.md`       | → `docs/ARCHITETTURA.md`     |
| `v4/docs/index.html`            | → `docs/index.html`          |
| `v4/docs/css/style.css`         | → `docs/css/style.css`       |
| `v4/docs/js/cards.js`           | → `docs/js/cards.js`         |
| `v4/docs/js/engine.js`          | → `docs/js/engine.js`        |
| `v4/docs/js/ui.js`              | → `docs/js/ui.js`            |

Dopo il caricamento:  
**https://pharaohshadow.github.io/Penumbra/**

---

**Versione:** v4 – Mano di carte + evocazione Creature  
**Data:** 24 ottobre 2026  
