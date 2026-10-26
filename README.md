# Penumbra – Consegna v19 (frontend + login)

Collegamento del frontend al login Supabase: il gioco manda sempre il token.

**Sito in costruzione.** Scelta A confermata.

## Cosa è stato fatto (in parole semplici)

Prima il gioco funzionava senza login.  
Ora:
1. Appare una schermata di **accedi / registrati**
2. Solo dopo il login si può creare partite e giocare
3. Ogni richiesta al server porta con sé il token dell’utente loggato

## Cosa devi fare tu

1. Carica il file `backend/static/index.html` di questa cartella nella repo (sostituisci quello esistente).
2. URL e chiave Supabase sono **già inseriti**.

## File di questa consegna

| File | Cosa fare |
|------|-----------|
| `backend/static/index.html` | **Sostituisci** quello esistente |
| `README.md` | Questo handoff |

## Come si usa dopo

1. Apri il sito
2. Registrati (o accedi) con email e password
3. Poi puoi creare partite vs IA o PvP e giocare normalmente

## Nota

Gli utenti di test si possono creare anche dalla dashboard Supabase (Authentication → Users), se preferisci non usare la registrazione dalla pagina.
