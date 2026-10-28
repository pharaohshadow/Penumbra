# Roadmap – Penumbra

**Versione attuale: v1.11**

## Stato attuale
v1.11 – Montagne irregolari (poligoni a cresta) al posto delle linee.

---

## 1. Sistema di consegne e documentazione
**Stato: CHIUSO**

---

## 2. Mappa esagonale e logica

### 2.1 Core mappa
- [x] Coordinate hex + parse_hex_key + hex_to_pixel
- [x] Muri scelti dall’utente (map.json)
- [x] Fix Fog of War (v1.10)
- [x] Montagne irregolari in UI (v1.11)
- [ ] Verificare movimento / blocco montagne in game_state e map_board
- [ ] Verificare spawn tempio / altare / draft

### 2.2 Logica di gioco
- [ ] Controllare che le montagne blocchino davvero il passaggio
- [ ] Controllare che la nebbia nasconda unità e nomi caselle

---

## 3. Stile grafico della mappa

### 3.1 Montagne
- [x] Forme a cresta irregolare (non linee)
- [x] Colori roccia + luce sulla cresta
- [ ] Eventuale ritocco spessore/altezza dopo feedback utente
- [ ] Bordo esterno: stessi poligoni montagna (non solo caselle colorate)

### 3.2 Tessere e terreno
- [x] Esagoni uniti
- [ ] Palette terreno più leggibile
- [ ] Icone piccole e coerenti
- [ ] Altare e templi più riconoscibili

### 3.3 Fog of war (aspetto)
- [x] Colore diverso dalle montagne
- [ ] Nebbia più “fumo”
- [ ] Nessun nome leggibile sotto la nebbia

### 3.4 UI intorno alla mappa
- [ ] Scalabilità mobile
- [ ] Feedback selezione / movimento
- [ ] Unità più leggibili

### 3.5 Ordine consigliato
1. ~~Montagne irregolari (3.1)~~ ← fatto in v1.11
2. Feedback utente sulle montagne → ritocco se serve
3. Icone terreno + palette (3.2)
4. Nebbia soft (3.3)
5. Polish UI (3.4)

---

## 4. Fuori scope finché non lo chiedi
- PvP completo
- Tutorial / Storia / Endless
