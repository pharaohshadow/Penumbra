# Architettura – Penumbra v7

## Novità v7

- Più partite in memoria: `game_id` (UUID)
- `POST /api/new` con `vs_ai: true|false`
- `POST /api/join` per secondo umano
- UI: bottoni Nuova vs IA / Nuova PvP / Unisciti
- Tutte le mosse richiedono `game_id` + `player_id`

## Limiti attuali

- Stato partita in RAM sul dyno Render (perso a sleep/restart)
- PvP solo se entrambi sono sulla stessa istanza attiva
- Supabase salva snapshot ma non ancora reload completo all’avvio

## Prossimi passi

1. Reload partita da Supabase `state_json` via `game_id`
2. Polling o Realtime per aggiornare la UI del guest senza refresh
3. Auth Supabase

**Versione: v7**
