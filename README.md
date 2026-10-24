# Penumbra

**Gioco di carte tattico egizio su griglia**  
Partite veloci (~5 minuti) – Browser – Grafica stile Yu-Gi-Oh Duel Links

---

## Cos’è Penumbra

Penumbra è un gioco di carte a turni ambientato nell’antico Egitto.  
Si gioca su una **griglia 4×5**.  
Il movimento e il posizionamento sono fondamentali (come negli scacchi + Mage Wars Arena).

Ogni giocatore controlla:
- La propria **pedina** (il Magus) che sta sempre sulla griglia
- Creature, Torri e Armi che piazza sulla griglia
- Maledizioni e Trappole che gioca “in aria”

L’obiettivo è **ridurre a 0 i punti vita** del Magus avversario.

---

## Stato attuale – v2

**Giocabile!**  
Apri `docs/index.html` (o il sito GitHub Pages) e puoi già:

- Vedere la griglia 4×5 con tema egizio scuro
- Muovere il tuo Magus (clicca → caselle evidenziate → clicca destinazione)
- Vedere le barre vita e il sistema Powa
- Passare il turno (l’IA fa una mossa semplice e torna a te)

**Ancora non implementato in v2:**
- Carte in mano
- Attacco melee
- Creature / Torri / Armi
- Effetti e Cimitero
- Vittoria/sconfitta completa

---

## Regole principali

### Griglia
- 4 righe × 5 colonne
- Non si può stare sulla stessa casella
- Tutti i pezzi (incluso il Magus) si muovono di **1 passo solo ortogonale**

### Il Magus (il giocatore)
- 20 Punti Vita
- 1 di Attacco
- Può muoversi e attaccare in melee

### Tipi di carte

**Permanenti**
- **Creature** (Mostri / Mostrissimi) → Attacco + Vita
- **Torri** → Solo Vita + abilità passive (non si muovono)
- **Armi** → Equipaggiamento. Occupano “mani”

**Non permanenti**
- **Maledizioni** → solo nel proprio turno (“in aria”)
- **Trappole** → solo nel turno dell’avversario (“in aria”)

### Mana (Powa)
- Turno 1: entrambi partono con 1 Powa
- All’inizio del proprio turno guadagni Powa pari al numero del turno
- Massimo 6 Powa in riserva
- Il Powa non speso **non si perde mai**

### Mano
- 10 carte già in mano dall’inizio
- Non si pesca

### Combattimento
- Solo melee (caselle adiacenti ortogonali)
- Danno = Attacco dell’attaccante
- Alla morte → Cimitero + eventuali effetti “on death”

### Vittoria
- Solo riducendo a 0 i Punti Vita del Magus avversario

---

## Stack tecnico

| Parte              | Tecnologia          | Note                                      |
|--------------------|---------------------|-------------------------------------------|
| Frontend           | HTML + CSS + JS     | Hostato su **GitHub Pages** (cartella `docs`) |
| Utenti + Carte     | **Supabase**        | Auth + database carte (prossimamente)     |
| Backend (se serve) | **Render**          | Solo se servono partite online            |
| Grafica            | CSS moderno + animazioni | Stile Yu-Gi-Oh Duel Links             |

---

## Struttura file (v2)

```
docs/
├── index.html
├── ARCHITETTURA.md
├── css/
│   └── style.css
└── js/
    ├── engine.js   ← logica di gioco
    └── ui.js       ← interfaccia e input
```

---

## Roadmap

**Fase 1 – Fondamenta** → FATTA (v1)  
**Fase 2 – Partita base VS IA** → IN CORSO  
- [x] Griglia funzionante  
- [x] Movimento Magus  
- [x] Sistema turni + Powa  
- [ ] Combattimento melee  
- [ ] Mano di 10 carte  
- [ ] IA più intelligente  

**Fase 3 – Carte e bilanciamento**  
**Fase 4 – Modalità** (Endless, Storia, PvP)

---

## Come caricare questa versione su GitHub

1. Vai su https://github.com/pharaohshadow/Penumbra
2. Carica i file della cartella `v2` mantenendo la struttura:

| File locale                     | Dove metterlo sul repository      |
|---------------------------------|-----------------------------------|
| `v2/README.md`                  | → root (`README.md`)              |
| `v2/docs/ARCHITETTURA.md`       | → `docs/ARCHITETTURA.md`          |
| `v2/docs/index.html`            | → `docs/index.html`               |
| `v2/docs/css/style.css`         | → `docs/css/style.css`            |
| `v2/docs/js/engine.js`          | → `docs/js/engine.js`             |
| `v2/docs/js/ui.js`              | → `docs/js/ui.js`                 |

Dopo il caricamento il gioco sarà giocabile su:  
**https://pharaohshadow.github.io/Penumbra/**

---

**Ultimo aggiornamento:** 24 ottobre 2026  
**Versione:** v2 – Griglia + movimento Magus + turni + Powa  
