# Architettura – v30

## Neutrali
- `neutral_colors_used: List[Color]`
- `_spawn_altar_neutral` / `_spawn_signore` / `_activate_altar_neutrals` a fine `end_turn`
- Stats da media globale mostri giocatori
- Signore: `signore_atk`, `signore_appearances`, status `signore|untargetable|immortal`

## Artefatto / indizi
- `Tile.has_artifact`
- `Player.clues`
- `_try_pickup_artifact` in `_on_enter_tile`
- `pending_popups` serializzati una volta poi cleared

## Fog / mappa
Come v28–v29.
