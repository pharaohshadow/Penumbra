# Istruzioni per IA – Penumbra — preferenze permanenti

## Contesto prodotto (NON chiedere di nuovo)

- Il sito è **in costruzione**.
- **Non** ci sono partite in corso né utenti che giocano davvero.
- Si può fare hard cut senza migrazioni soft per i giocatori.
- L’utente **non è competente in informatica**: non mostrare diff tecnici, non spiegare codice riga per riga. Fornisci sempre file pronti e istruzioni semplici in italiano.

## Auth / membership (NON chiedere di nuovo)

- **Scelta A:** partite senza membership valida per l’uid del JWT → **403**.
- Niente `ALLOW_LEGACY_OPEN`.
- Niente spectator.
- Partita base: vs IA, P0 = utente loggato.
- Frontend manda sempre `Authorization: Bearer <access_token>`.

## Consegne

- File pronti da scaricare, italiano, niente diff complicati.
- “Procedi” / “Fai finta e procedi” → micro-step successivo.

## Stato

- 4.2 API protetta: completa
- Frontend login: fatto in v19
