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

## Regole principali (v1)

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
- **Creature** (Mostri / Mostrissimi) → hanno Attacco e Vita
- **Torri** → hanno solo Vita + abilità passive (non si muovono)
- **Armi** → equipaggiamento. Occupano “mani”. Le creature hanno un numero di mani (alcune ne hanno di più)

**Non permanenti**
- **Maledizioni** → si giocano solo nel proprio turno (effetto immediato “in aria”)
- **Trappole** → si giocano solo nel turno dell’avversario (effetto immediato “in aria”)

### Mana (Powa)
- All’inizio del turno 1 entrambi i giocatori hanno 1 Powa
- All’inizio del proprio turno il giocatore guadagna Powa pari al **numero del turno**
- Massimo 6 Powa in riserva
- Il Powa non speso **non si perde mai**

### Mano
- Ogni giocatore inizia con **10 carte** già in mano
- **Non si pesca** durante la partita (come Mage Wars Arena)

### Combattimento
- Si attacca solo in **melee** (casella adiacente ortogonale)
- Il danno inflitto è pari all’Attacco della creatura
- Quando una creatura muore va al **Cimitero** e attiva eventuali effetti “on death”

### Vittoria
- Si vince **solo** riducendo a 0 i Punti Vita del Magus avversario

---

## Stack tecnico

| Parte              | Tecnologia          | Note                                      |
|--------------------|---------------------|-------------------------------------------|
| Frontend           | HTML + CSS + JS     | Hostato su **GitHub Pages** (cartella `docs`) |
| Utenti + Carte     | **Supabase**        | Auth + database carte                     |
| Backend (se serve) | **Render**          | Solo se servono partite online o logica complessa |
| Grafica            | CSS moderno + animazioni | Stile Yu-Gi-Oh Duel Links – figo e fluido |

---

## Roadmap attuale

**Fase 1 – Fondamenta (questa versione)**  
- Documentazione completa  
- Struttura del progetto  

**Fase 2 – Partita base VS IA**  
- Griglia funzionante  
- Movimento  
- Combattimento melee  
- Sistema Powa  
- Mano di 10 carte  
- IA semplice  

**Fase 3 – Carte e bilanciamento**  
- Primi set di carte (parodie)  
- Effetti on death, abilità passive torri, armi  

**Fase 4 – Modalità**  
- Endless  
- Storia  
- PvP vero  

---

## Come caricare questa versione su GitHub

1. Vai su https://github.com/pharaohshadow/Penumbra
2. Carica i file della cartella `v1` mantenendo la stessa struttura:
   - `README.md` → nella root del repository
   - `docs/ARCHITETTURA.md` → dentro la cartella `docs`

---

**Ultimo aggiornamento:** 24 ottobre 2026  
**Versione:** v1 – Solo documentazione di base  
