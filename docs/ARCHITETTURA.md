# ARCHITETTURA – Penumbra v3

Documento di riferimento completo.  
Leggendo questo file + il README si può riprendere il lavoro da zero in qualsiasi momento.

---

## 1. Visione del gioco

Penumbra è un **card game tattico a turni** ambientato nell’Egitto antico.

Ispirazioni principali:
- **Mage Wars Arena** → griglia + tutte le carte già in mano + movimento
- **Yu-Gi-Oh Duel Links** → aspetto grafico figo e fluido
- **Scacchi** → importanza del posizionamento

Partite corte (circa 5 minuti).  
Prima implementazione: **partita base contro IA**.  
In futuro le modalità (Endless, Storia, PvP) nasceranno aggiungendo **modificatori** alla partita base.

---

## 2. Regole complete (fonte di verità)

### 2.1 Griglia
- Dimensioni: **4 righe × 5 colonne**
- Orientamento: più larga che alta
- Nessuna unità può occupare la stessa casella
- Movimento: **1 solo passo ortogonale**

### 2.2 Il Magus
- 20 Punti Vita – 1 di Attacco
- Può muoversi e attaccare
- Ogni unità può fare **una sola azione per turno** (muovere **oppure** attaccare)

### 2.3 Tipi di carte (ancora non implementati nel codice)

#### Permanenti
| Tipo       | Caratteristiche                                      |
|------------|------------------------------------------------------|
| Creature   | Attacco + Vita. Sottocategorie: Mostri / Mostrissimi |
| Torri      | Solo Vita + abilità passive. Non si muovono          |
| Armi       | Equipaggiamento. Occupano un certo numero di “mani”  |

#### Non permanenti
| Tipo       | Quando si gioca              | Dove si gioca |
|------------|------------------------------|---------------|
| Maledizioni| Solo nel proprio turno       | “In aria”     |
| Trappole   | Solo nel turno dell’avversario| “In aria”    |

### 2.4 Sistema Powa
- Turno 1: entrambi partono con **1 Powa**
- All’inizio del proprio turno guadagni Powa pari al **numero del turno**
- Massimo **6 Powa** in riserva
- Il Powa non speso **non viene mai perso**

### 2.5 Mano
- Ogni giocatore inizia con **10 carte**
- Non esiste la pesca

### 2.6 Combattimento
- Solo **melee** (caselle adiacenti ortogonali)
- Danno = valore di Attacco dell’attaccante
- Quando un’unità muore:
  1. Va nel **Cimitero**
  2. Si attivano eventuali effetti **“on death”** (futuro)

### 2.7 Condizione di vittoria
- Unica: ridurre a **0** i Punti Vita del Magus avversario

---

## 3. Architettura tecnica

### 3.1 Frontend
- Cartella `docs/` hostata su **GitHub Pages**
- HTML + CSS + JavaScript vanilla
- Grafica moderna stile Yu-Gi-Oh Duel Links

### 3.2 Backend / Dati
| Servizio   | Uso                                      |
|------------|------------------------------------------|
| **Supabase** | Autenticazione utenti + database carte  |
| **Render**   | Solo se in futuro servono partite online |

### 3.3 Struttura file attuale (v3)

```
docs/
├── index.html
├── ARCHITETTURA.md
├── css/
│   └── style.css
└── js/
    ├── engine.js   ← logica pura (stato, movimento, attacco, turni, IA, vittoria)
    └── ui.js       ← rendering + gestione click
```

### 3.4 Separazione responsabilità
- **engine.js** → nessuna conoscenza del DOM. Solo regole e stato.
- **ui.js** → legge `Game.getState()` e aggiorna la pagina. Invia comandi all’engine.

---

## 4. Cosa funziona in v3

- Griglia 4×5
- Due Magus con HP e ATK
- Selezione unità (solo se non ha ancora agito)
- Evidenziazione **gialla** = caselle di movimento
- Evidenziazione **rossa** = caselle di attacco
- Movimento (1 passo ortogonale)
- Attacco melee → applica danno
- Morte → unità rimossa e messa nel Cimitero
- Controllo vittoria/sconfitta
- Schermata fine partita + pulsante Rigioca
- IA: attacca se adiacente, altrimenti si avvicina
- Ogni unità può fare una sola azione per turno (`acted`)
- Sistema turni + Powa

---

## 5. Cosa manca ancora (prossima v4)

1. **Mano di 10 carte** visualizzata in basso
2. **Giocare la prima Creatura** (pagando Powa, piazzandola su casella adiacente al Magus)
3. Creature con ATK/HP diversi
4. IA che gioca anche creature semplici
5. Effetti “on death” base

---

## 6. Decisioni di design già prese

- Partita base = VS IA
- Modalità future = modificatori della partita base
- Carte = parodie di Pokémon, Yu-Gi-Oh, Magic ecc.
- Grafica prioritaria: deve sembrare un vero videogioco
- Un’azione per unità per turno (muovere **oppure** attaccare)

---

## 7. Note per lo sviluppatore futuro

- L’utente **non è tecnico**. Non chiedergli modifiche manuali complesse su GitHub.
- Ogni consegna di file:
  - Creare cartella `v4`, `v5`…
  - Mettere dentro README aggiornato + ARCHITETTURA aggiornata + tutti i file da pushare
- Prima di toccare file critici (`engine.js`, `ui.js`) rileggerli sempre.

---

**Versione documento:** v3  
**Data:** 24 ottobre 2026  
**Stato:** Attacco melee + danni + vittoria/sconfitta funzionanti  
