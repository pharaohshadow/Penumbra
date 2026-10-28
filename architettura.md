# Architettura – v29

## Consegne
Cartelle `penumbra_vXX` progressive; non sovrascrivere versioni precedenti.

## Neutrali Altare
- `GameState.neutral_tier` (0..6): ultimo tier spawnato
- A `end_turn`: `_activate_altar_neutrals()` poi `_spawn_altar_neutral()`
- Spawn su `ALTAR_POS` se libera
- Unit `owner_id == -1`, status `altar_neutral`; tier 6 → anche `signore`
- Bersaglio in status `target:COORD` / `target:none`
- Visione neutrali: Chebyshev ≤ 2 dalla propria posizione

## Fog of War / Mappa
Come v28.3 (raggio 2, edge walls, 7×7, templi angoli).

## Corona
`_sync_fragment_card` mantiene carta Frammento in mano.
