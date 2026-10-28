# Architettura – v33

## Hex
- `constants.HEX_RADIUS=3`, `all_hexes`, `hex_distance`, `hex_to_pixel`
- `Board.tiles: Dict[(q,r), Tile]`, `edge_walls` su coppie hex
- Serialize: lista piatta di celle con `coord` (flavor), `qr`, `x/y`

## UI
- Hex con `clip-path` pointy, posizionati in pixel
- Player panel in basso + medaglione
- Eldrazi box nascosto finché non su rituale

## Compatibilità
- Alcuni path legacy (eventi/trappole) restano nel codice ma le caselle non li usano più
