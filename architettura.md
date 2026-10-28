# Architettura – v28

## Mappa 7×7

- Griglia **7×7** (coordinate A–G / 0–6)
- Zona giocabile interna: righe 1–5, colonne 1–5
- Cornice esterna `TileType.FRAME` → non camminabile
- **Templi agli angoli**:
  - TEMPIO 1 (P0 umano) = (6, 0) basso-sinistra
  - TEMPIO 2 (P1 IA) = (0, 6) alto-destra
  - TEMPIO 3 e 4 presenti per futuro 4 giocatori
- **Altare** = (3, 3) centro zona MAPPA
- **Spawn** creature gratuite e unità iniziali: **solo** sulla casella del Tempio del giocatore

## Muri edge (non più celle)

- I muri non occupano una casella
- Sono barriere tra due celle adiacenti (`Board.edge_walls`)
- Movimento ortogonale bloccato se esiste il muro edge
- Movimento diagonale bloccato se entrambi i percorsi ortogonali sono murati
- Layout muri = esattamente i bordi blu dell’xlsx fornito dall’utente
- UI: linee scure (bordo più marcato / overlay)

## UI partita

- Niente pulsanti Nuova PvP / Unisciti / Piazza Corona
- Home resta il posto per le modalità
- Griglia visualizzata 7×7

## Corona

- Carta `CardType.FRAGMENT` in mano, costo 0 / 3 / 6
- `play_card` → `_play_fragment` → `place_fragment` + `_sync_fragment_card`
- Dopo perdita frammento, la carta può tornare in mano se ne restano

## Draft

- Buste sigillate (v26)

## Auth

- Login obbligatorio (JWT Supabase)
- Nessuna modalità anonima
