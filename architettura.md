# Architettura – v31

- UI: skip `TileType.FRAME`; grid 7×7 con solo celle utili posizionate.
- `edge_walls`: muri xlsx + perimetro playable (1..5)×(1..5) verso cornice.
- `try_move`: check muro prima di move/combat.
- Spawn free: nome `Soldato` (stats solo in UI).
