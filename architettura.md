# Architettura – v28.3

## Mappa 7×7
- Griglia 7×7 (A–G / 0–6), zona giocabile 5×5 interna
- Cornice FRAME non camminabile
- Templi: P0 = A6 (6,0), P1 = G0 (0,6)
- Altare D3 (3,3)
- Spawn solo sul Tempio
- Muri = edge walls (non celle)

## Fog of War
- Raggio Chebyshev 2 da creature del giocatore + Tempio
- `GameState.is_visible_to(player_id, row, col)`
- `serialize_state(..., viewer_id)` nasconde unità/tile fuori visione
- Maledizioni a bersaglio nemico: bloccate se `not can_target_unit`

## Neutrali
- Rimossi: niente `_spawn_neutral` / `_activate_neutrals` a inizio turno

## Corona
- Carta FRAGMENT in mano, costo 0/3/6
- `_sync_fragment_card` mantiene la carta in mano aggiornata

## Auth
- JWT obbligatorio
