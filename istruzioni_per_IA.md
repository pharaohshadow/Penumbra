# Istruzioni per IA – Penumbra (v12) — preferenze permanenti

## Contesto prodotto (NON chiedere di nuovo)

- Il sito è **in costruzione**.
- **Non** ci sono partite in corso né utenti che giocano davvero.
- Si può fare hard cut senza migrazioni soft per i giocatori.

## Auth / membership (NON chiedere di nuovo)

- **Scelta A:** partite senza membership valida per l’uid del JWT → **403**.
- Niente `ALLOW_LEGACY_OPEN`.
- Niente spectator.
- Partita base: vs IA, P0 = utente loggato.

## Consegne

- Cartelle `vN` con README handoff, ROADMAP, architettura, istruzioni_per_IA.
- Non rompere il motore di gioco; auth è un gate attorno.
- Italiano.

## Roadmap attiva

- 4.2.1 fatto → proseguire 4.2.2, 4.2.3, … salvo diversa istruzione.
- “Fai finta e procedi” / “Procedi” → micro-step successivo.
