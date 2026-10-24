# ARCHITETTURA – Penumbra v1

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
- HTML + CSS + JavaScript vanilla (o con librerie leggere se servono)
- Grafica moderna, animazioni fluide, stile Yu-Gi-Oh Duel Links

### 3.2 Backend / Dati
| Servizio   | Uso                                      |
|------------|------------------------------------------|
| **Supabase** | Autenticazione utenti + database carte  |
| **Render**   | Solo se in futuro servono partite online in tempo reale o logica server-side complessa |

### 3.3 Struttura cartelle prevista (futura)

```
/
├── README.md
├── docs/
│   ├── index.html          ← pagina principale del gioco
│   ├── ARCHITETTURA.md
│   ├── css/
│   ├── js/
│   │   ├── engine/         ← logica di gioco pura
│   │   ├── ui/             ← interfaccia
│   │   └── ai/             ← intelligenza artificiale
│   └── assets/             ← immagini, suoni, font
```

---

## 4. Decisioni di design già prese

- Partita base = VS IA (un giocatore umano + un giocatore controllato dall’IA)
- Le modalità future (Endless, Storia, PvP) saranno **modificatori** della partita base
- Le carte saranno **parodie** di carte famose (Pokémon, Yu-Gi-Oh, Magic ecc.)
- Grafica prioritaria: deve sembrare un vero videogioco, non un prototipo grezzo

---

## 5. Prossimi passi (dopo v1)

1. Creare la struttura base del frontend (griglia 4×5 + Magus)
2. Sistema di turni e Powa
3. Movimento delle unità
4. Sistema di attacco melee
5. Mano di 10 carte + gioco delle carte
6. IA molto semplice (muove e attacca in modo basico)
7. Schermata di vittoria / sconfitta

---

## 6. Note per lo sviluppatore futuro

- L’utente **non è tecnico**. Non chiedergli di fare modifiche manuali complesse su GitHub.
- Ogni volta che si consegnano file da caricare:
  - Creare una cartella `v2`, `v3`…
  - Mettere dentro README aggiornato + ARCHITETTURA aggiornata + tutti i file da pushare
- Prima di toccare file critici, rileggerli sempre.

---

**Versione documento:** v1  
**Data:** 24 ottobre 2026  
**Stato:** Solo documentazione – nessun codice ancora scritto  
