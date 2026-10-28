# Roadmap – Penumbra

**Versione attuale: v1.1**

Questo file viene aggiornato obbligatoriamente a ogni consegna.  
Indica lo stato reale dei lavori.

---

## Stato attuale
v1.1 – Hotfix di stabilizzazione.  
Risolti gli errori di importazione (`HexPos`, `hex_neighbors`, `hex_in_radius`, ecc.) che impedivano l’avvio su Render.

---

## 1. Sistema di consegne e documentazione (completato)

- [x] 1.1 Creare i 4 file di base
- [x] 1.2 Verificare lettura corretta dei 4 file
- [x] 1.3 Completare URL di Supabase e Render
- [x] 1.4 Definire i prossimi punti di lavoro

**Stato: CHIUSO**

---

## 2. Migrazione completa alla mappa esagonale (in corso)

### 2.1 Core della mappa
- [x] 2.1.1 Sistema coordinate esagonali + compatibilità (`HexPos`, `hex_neighbors`, `hex_in_radius`…)
- [ ] 2.1.2 Caricamento e validazione di `map.json`
- [ ] 2.1.3 Riscrivere `Tile` per tipi esagonali + muri tra celle
- [ ] 2.1.4 Riscrivere completamente `Board` (`map_board.py`) per esagoni
- [ ] 2.1.5 Aggiornare `Unit` (da row/col a q/r)

### 2.2 Logica di gioco
- [ ] 2.2.1 Adattare spawn templi e unità gratuite
- [ ] 2.2.2 Movimento esagonale (6 direzioni)
- [ ] 2.2.3 Gestione muri
- [ ] 2.2.4 Altare centrale e effetti di tessera
- [ ] 2.2.5 Spawn neutrali e attivazione
- [ ] 2.2.6 Sistema Corona/Frammenti su mappa esagonale

### 2.3 API e serializzazione
- [ ] 2.3.1 Aggiornare `serialize_state`
- [ ] 2.3.2 Adattare restore/hydrate
- [ ] 2.3.3 Verificare compatibilità con Supabase

### 2.4 Frontend
- [ ] 2.4.1 Rendering mappa esagonale
- [ ] 2.4.2 Click e selezione
- [ ] 2.4.3 Feedback visivo muri e tessere

### 2.5 Stabilizzazione
- [ ] 2.5.1 Aggiornare AI base
- [ ] 2.5.2 Smoke test completo
- [ ] 2.5.3 Pulizia codice residuo 5×5

---

## 3. Stabilizzazione e rifinitura Partita base (da iniziare)

(Da definire dopo la chiusura del punto 2)

---

## Rischi e note
- L’utente non è tecnico → ogni passaggio deve essere semplice e guidato.
- È fondamentale non perdere i dettagli di Supabase e Render.
- La migrazione della mappa tocca quasi tutto il codice: procedere per piccoli passi verificabili.
