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

## Stato attuale – v3

**Giocabile con combattimento!**

Cosa puoi fare:
- Muovere il Magus (caselle **gialle**)
- Attaccare in melee (caselle **rosse**)
- Vedere i danni e gli HP sulle unità
- L’IA attacca se ti avvicini, altrimenti si avvicina
- Vittoria / Sconfitta quando un Magus arriva a 0 HP
- Pulsante **Rigioca**

**Ancora non implementato:**
- Carte in mano
- Creature / Torri / Armi
- Effetti “on death”
- Sistema Powa per giocare carte

---

## Regole principali

### Griglia
- 4 righe × 5 colonne
- Non si può stare sulla stessa casella
- Tutti i pezzi si muovono di **1 passo solo ortogonale**

### Il Magus
- 20 Punti Vita – 1 di Attacco
- Può muoversi e attaccare in melee
- Ogni unità può fare **una sola azione per turno** (muovere **oppure** attaccare)

### Combattimento
- Solo **melee** (caselle adiacenti ortogonali)
- Danno = Attacco dell’attaccante
- Alla morte → va nel **Cimitero**

### Mana (Powa)
- Turno 1: entrambi partono con 1 Powa
- All’inizio del proprio turno guadagni Powa pari al numero del turno (max 6)
- Il Powa non speso non si perde

### Vittoria
- Solo riducendo a 0 i Punti Vita del Magus avversario

---

## Stack tecnico

| Parte              | Tecnologia          | Note                                      |
|--------------------|---------------------|-------------------------------------------|
| Frontend           | HTML + CSS + JS     | Hostato su **GitHub Pages** (cartella `docs`) |
| Utenti + Carte     | **Supabase**        | Auth + database carte (prossimamente)     |
| Backend (se serve) | **Render**          | Solo se servono partite online            |

---

## Struttura file (v3)

```
docs/
├── index.html
├── ARCHITETTURA.md
├── css/
│   └── style.css
└── js/
    ├── engine.js   ← logica di gioco (movimento, attacco, turni, IA)
    └── ui.js       ← interfaccia e input
```

---

## Roadmap

**Fase 1 – Fondamenta** → FATTA (v1)  
**Fase 2 – Griglia + movimento** → FATTA (v2)  
**Fase 3 – Attacco melee** → FATTA (v3)  
**Prossima (v4)** → Mano di carte + giocare la prima Creatura  

---

## Come caricare questa versione su GitHub

1. Vai su https://github.com/pharaohshadow/Penumbra
2. Carica i file della cartella `v3` mantenendo la struttura:

| File locale                        | Dove metterlo sul repository       |
|------------------------------------|------------------------------------|
| `v3/README.md`                     | → **root** (`README.md`)           |
| `v3/docs/ARCHITETTURA.md`          | → `docs/ARCHITETTURA.md`           |
| `v3/docs/index.html`               | → `docs/index.html`                |
| `v3/docs/css/style.css`            | → `docs/css/style.css`             |
| `v3/docs/js/engine.js`             | → `docs/js/engine.js`              |
| `v3/docs/js/ui.js`                 | → `docs/js/ui.js`                  |

Dopo il caricamento il gioco sarà qui:  
**https://pharaohshadow.github.io/Penumbra/**

---

**Ultimo aggiornamento:** 24 ottobre 2026  
**Versione:** v3 – Attacco melee + danni + vittoria/sconfitta  
