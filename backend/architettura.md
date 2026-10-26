# Architettura – Penumbra v8

## v8
- `static/index.html`: `setInterval` 2.5s su `/api/state` se `current_player !== playerId`
- `game_state._resolve_portal`: teletrasporto Bianco↔Nero (o primo portale disponibile)

## Prossimi
1. Reload da Supabase `state_json`
2. Realtime Supabase al posto del polling
3. Auth

**Versione: v8**
