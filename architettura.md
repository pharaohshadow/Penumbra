# Architettura – v27

## UI partita
- Niente pulsanti Nuova PvP / Unisciti / Piazza Corona
- Home resta il posto per le modalità

## Corona
- Carta `CardType.FRAGMENT` in mano, costo 0 / 3 / 6
- `play_card` → `_play_fragment` → `place_fragment` + `_sync_fragment_card`
- Dopo perdita frammento, la carta può tornare in mano se ne restano

## Draft
- Buste sigillate (v26)
