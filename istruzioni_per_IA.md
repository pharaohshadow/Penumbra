# Istruzioni per IA – Penumbra

- Utente non tecnico; niente modifiche manuali; aggiornare README/ROADMAP/architettura/istruzioni ogni volta.
- UI partita: niente PvP/Unisciti finché non si lavora su quella modalità.
- Corona = carta in mano costo 0/3/6, non bottone dedicato.
- Draft = buste; movimento = re; Giallo = proxy.
- **Mappa v28**: griglia 7×7, templi agli angoli, cornice non giocabile, muri = edge walls (non celle), spawn solo sul Tempio, Altare al centro (3,3), coordinate A–G / 0–6.
- Auth obbligatorio (Supabase JWT).
- Fase A (errori 400/500) rimandata: l’utente rifà una partita e segnala se l’errore del 3° turno si ripresenta.
