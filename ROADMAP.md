# Roadmap – Penumbra

**Versione attuale: v1.10**

## Stato attuale
v1.10 – Fix Fog of War (non si vede più “per sbaglio” la zona del tempio avversario).  
Grafica: base ok, ma montagne e stile generale da migliorare (sezione 3).

---

## 1. Sistema di consegne e documentazione
**Stato: CHIUSO**

---

## 2. Mappa esagonale e logica

### 2.1 Core mappa
- [x] Coordinate hex + `parse_hex_key` + `hex_to_pixel`
- [x] Muri scelti dall’utente (map.json)
- [x] Fix Fog of War (v1.10)
- [ ] Verificare movimento / blocco montagne in game_state e map_board
- [ ] Verificare spawn tempio / altare / draft dopo fix vision

### 2.2 Logica di gioco
- [ ] Controllare che le montagne blocchino davvero il passaggio
- [ ] Controllare che la nebbia nasconda unità e nomi caselle

---

## 3. Stile grafico della mappa (priorità utente)

Obiettivo: mappa bella, chiara, “da gioco”, non linee tecniche.

### 3.1 Montagne (prossimo passo consigliato)
- [ ] Sostituire le **linee** con forme di **cresta irregolare** (poligoni SVG o path a spezzata)
- [ ] Colori roccia realistici (marrone/grigio con luci e ombre)
- [ ] Leggera irregolarità per lato (non tutte uguali)
- [ ] Opzionale: piccola silhouette ⛰ stilizzata sui tratti lunghi
- [ ] Bordo esterno: stesse montagne, non solo caselle colorate

### 3.2 Tessere e terreno
- [x] Esagoni uniti (niente buchi neri)
- [ ] Palette terreno più leggibile (bosco / lago / rovina distinti a colpo d’occhio)
- [ ] Icone piccole e coerenti (non solo testo schiacciato)
- [ ] Altare e templi più riconoscibili (già giallo/verde, da raffinare)

### 3.3 Fog of war (aspetto)
- [x] Colore diverso dalle montagne
- [ ] Nebbia più “fumo” (gradiente / opacità) invece di casella piatta scura
- [ ] Nessun nome leggibile sotto la nebbia

### 3.4 UI intorno alla mappa
- [ ] Scalabilità mobile (la mappa resta leggibile su telefono)
- [ ] Feedback selezione casella / movimento più chiaro
- [ ] Unità più leggibili (nome + atk/hp senza sovrapporsi)

### 3.5 Passo dopo passo (ordine consigliato)
1. **Montagne irregolari** (3.1) ← prossimo lavoro grafico
2. Icone terreno + palette (3.2)
3. Nebbia più soft (3.3)
4. Polish UI (3.4)

---

## 4. Fuori scope finché non lo chiedi
- PvP completo
- Tutorial / Storia / Endless

---

## Rischi e note
- L’utente non è tecnico → ogni consegna deve essere una cartella pronta da caricare.
- Prima di toccare file critici (`game_state.py`, `map_board.py`, `api/main.py`, `index.html`) rileggerli per intero.
