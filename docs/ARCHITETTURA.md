# ARCHITETTURA – Penumbra v2

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
- Movimento: **1 solo passo ortogonale** (su, giù, sinistra, destra) per tutti i pezzi

### 2.2 Il Magus (pedina del giocatore)
- È sempre presente sulla griglia
- 20 Punti Vita
- 1 di Attacco
- Può muoversi e attaccare come le altre creature
- Se i suoi Punti Vita arrivano a 0 → sconfitta

### 2.3 Tipi di carte

#### Permanenti
| Tipo       | Caratteristiche                                      |
|------------|------------------------------------------------------|
| Creature   | Attacco + Vita. Sottocategorie: Mostri / Mostrissimi |
| Torri      | Solo Vita + abilità passive. Non si muovono          |
| Armi       | Equipaggiamento. Occupano un certo numero di “mani”  |

- Le creature hanno un numero di **mani** (può variare)
- Se non ci sono mani libere non si può equipaggiare un’altra arma

#### Non permanenti
| Tipo       | Quando si gioca              | Dove si gioca |
|------------|------------------------------|---------------|
| Maledizioni| Solo nel proprio turno       | “In aria”     |
| Trappole   | Solo nel turno dell’avversario| “In aria”    |

### 2.4 Sistema Powa (mana)
- Turno 1: entrambi i giocatori partono con **1 Powa**
- All’inizio del proprio turno il giocatore guadagna Powa pari al **numero del turno**
- Massimo **6 Powa** in riserva
- Il Powa non speso **non viene mai perso**

### 2.5 Mano
- Ogni giocatore inizia con **esattamente 10 carte**
- Non esiste la pesca durante la partita

### 2.6 Combattimento
- Solo **melee** (caselle adiacenti ortogonali)
- Il danno inflitto = valore di Attacco dell’attaccante
- Quando una creatura (o torre) muore:
  1. Va nel **Cimitero**
  2. Si attiva eventuali effetti **“on death”**

### 2.7 Condizione di vittoria
- Unica: ridurre a **0** i Punti Vita del Magus avversario

---

## 3. Architettura tecnica

### 3.1 Frontend
- Cartella `docs/` hostata su **GitHub Pages**
- HTML + CSS + JavaScript vanilla
- Grafica moderna, animazioni fluide, stile Yu-Gi-Oh Duel Links

### 3.2 Backend / Dati
| Servizio   | Uso                                      |
|------------|------------------------------------------|
| **Supabase** | Autenticazione utenti + database carte  |
| **Render**   | Solo se in futuro servono partite online |

### 3.3 Struttura file attuale (v2)

```
docs/
├── index.html
├── ARCHITETTURA.md
├── css/
│   └── style.css
└── js/
    ├── engine.js   ← logica pura (stato, movimento, turni, IA base)
    └── ui.js       ← rendering griglia + gestione click
```

### 3.4 Separazione responsabilità
- **engine.js** → nessuna conoscenza del DOM. Solo regole e stato.
- **ui.js** → legge lo stato da `Game.getState()` e aggiorna la pagina. Invia comandi all’engine.

---

## 4. Cosa funziona in v2

- Griglia 4×5 visualizzata
- Due Magus posizionati (player in basso centro, AI in alto centro)
- Selezione del Magus del giocatore
- Evidenziazione caselle di movimento valide (ortogonali libere)
- Movimento del Magus
- Sistema turni
- Guadagno Powa all’inizio del turno (max 6)
- IA molto semplice: muove il proprio Magus verso il basso se possibile e passa
- Barre vita (ancora non modificabili dal gameplay)
- Interfaccia responsive e stilizzata

---

## 5. Cosa manca ancora (prossima v3)

1. **Attacco melee**  
   - Seleziona unità → evidenzia nemici adiacenti → clicca per attaccare  
   - Applica danno, gestione morte, Cimitero

2. **Mano di carte**  
   - 10 carte fisse all’inizio  
   - Visualizzazione in basso  
   - Giocare Creature / Torri / Armi pagando Powa

3. **IA migliorata**  
   - Attacca se può  
   - Gioca carte semplici

4. **Schermata vittoria / sconfitta**

5. **Collegamento Supabase** (carte e utenti) – può arrivare dopo

---

## 6. Decisioni di design già prese

- Partita base = VS IA
- Modalità future = modificatori della partita base
- Carte = parodie di Pokémon, Yu-Gi-Oh, Magic ecc.
- Grafica prioritaria: deve sembrare un vero videogioco

---

## 7. Note per lo sviluppatore futuro

- L’utente **non è tecnico**. Non chiedergli modifiche manuali complesse su GitHub.
- Ogni consegna di file:
  - Creare cartella `v3`, `v4`…
  - Mettere dentro README aggiornato + ARCHITETTURA aggiornata + tutti i file da pushare
- Prima di toccare file critici (`engine.js`, `ui.js`) rileggerli sempre.

---

**Versione documento:** v2  
**Data:** 24 ottobre 2026  
**Stato:** Griglia + movimento Magus + turni + Powa funzionanti  
