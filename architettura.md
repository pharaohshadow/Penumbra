# Architettura – 4.2 completa

- Health e static pubblici
- Tutto il resto gioco richiede JWT
- Membership: solo player0_uid e player1_uid possono agire
- Partite senza uid → 403 (scelta A)
- `/api/new` → crea e assegna player0
- `/api/join` → unisce e assegna player1 (solo PvP)
- Store Supabase salva ownership
- No spectator, no legacy open
- Contesto: sito in costruzione
