# Roadmap – Penumbra

**Versione attuale: v1.0**

Questo file viene aggiornato obbligatoriamente a ogni consegna.  
Indica lo stato reale dei lavori.

---

## Stato attuale
Inizio ufficiale della migrazione alla mappa esagonale.  
I 4 file di consegna sono stati ricostruiti da zero (v1.0).  
Avviata la Fase 2.1 (core della mappa esagonale).

---

## 1. Sistema di consegne e documentazione (completato)

- [x] 1.1 Creare i 4 file di base (README, architettura, istruzioni_per_IA, roadmap)
- [x] 1.2 Verificare che la nuova chat legga correttamente solo i 4 file
- [x] 1.3 Completare in `architettura.md` gli URL reali di Supabase e Render
- [x] 1.4 Definire i prossimi punti di lavoro della Partita base (migrazione mappa)

**Stato: CHIUSO**

---

## 2. Migrazione completa alla mappa esagonale (in corso)

Obiettivo: sostituire definitivamente la griglia quadrata 5×5 con la mappa esagonale definita in `backend/data/map.json`.

### 2.1 Core della mappa (priorità massima)
- [x] 2.1.1 Creare sistema di coordinate esagonali (axial q,r) in `hex_coords.py` + aggiornamenti a `constants.py`
- [ ] 2.1.2 Caricamento e validazione di `map.json`
- [ ] 2.1.3 Riscrivere `Tile` per supportare tipi esagonali + muri tra celle
- [ ] 2.1.4 Riscrivere completamente `Board` (`map_board.py`) per esagoni
- [ ] 2.1.5 Aggiornare `Unit` (da row/col a q/r)

### 2.2 Logica di gioco
- [ ] 2.2.1 Adattare spawn templi e unità gratuite
- [ ] 2.2.2 Movimento esagonale (6 direzioni)
- [ ] 2.2.3 Gestione muri (blocco tra celle)
- [ ] 2.2.4 Altare centrale e effetti di tessera
- [ ] 2.2.5 Spawn neutrali e attivazione
- [ ] 2.2.6 Sistema Corona/Frammenti su mappa esagonale

### 2.3 API e serializzazione
- [ ] 2.3.1 Aggiornare `serialize_state` in `api/main.py`
- [ ] 2.3.2 Adattare restore/hydrate
- [ ] 2.3.3 Verificare compatibilità con Supabase

### 2.4 Frontend
- [ ] 2.4.1 Rendering mappa esagonale in `index.html`
- [ ] 2.4.2 Click, selezione e evidenziazione caselle
- [ ] 2.4.3 Feedback visivo muri e tipi di tessera

### 2.5 Stabilizzazione
- [ ] 2.5.1 Aggiornare AI base
- [ ] 2.5.2 Smoke test completo della partita base
- [ ] 2.5.3 Pulizia codice residuo della vecchia 5×5

**Nota**: quando tutti i sotto-punti del punto 2 saranno completati, la chat deve chiedere conferma prima di passare al punto 3.

---

## 3. Stabilizzazione e rifinitura Partita base (da iniziare)

(Da definire dopo la chiusura del punto 2)

---

## Rischi e note
- L’utente non è tecnico → ogni passaggio deve essere semplice e guidato.
- È fondamentale non perdere i dettagli di Supabase e Render (devono restare scritti in `architettura.md`).
- La migrazione della mappa tocca quasi tutto il codice: procedere per piccoli passi verificabili.
