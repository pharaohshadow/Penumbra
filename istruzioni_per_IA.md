# Istruzioni per IA – Penumbra — preferenze permanenti

## Contesto prodotto (NON chiedere di nuovo)

- Il sito è **in costruzione**.
- **Non** ci sono partite in corso né utenti che giocano davvero.
- Si può fare hard cut senza migrazioni soft per i giocatori.
- L’utente **non è competente in informatica**: file pronti, istruzioni semplici in italiano, niente diff tecnici.

## Auth / membership (NON chiedere di nuovo)

- **Scelta A:** senza membership → **403**.
- Niente legacy open, niente spectator.
- Frontend manda sempre Bearer token.
- 4.2 API protetta: completa. Frontend login: fatto.

## Consegne

- “Procedi” / “Fai finta e procedi” → micro-step utile successivo, spiegato in parole semplici.
