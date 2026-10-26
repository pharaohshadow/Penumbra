# Penumbra – Consegna v20 (go-live / checklist)

Checklist per far funzionare login + partite in produzione.

**Sito in costruzione.** Nessun giocatore reale da preservare.

## 1. Variabili su Render (backend)

Nel servizio Render del backend, imposta queste variabili d’ambiente:

| Variabile | Dove la prendi | A cosa serve |
|-----------|----------------|--------------|
| `SUPABASE_URL` | Supabase → Settings → API → Project URL | Collegamento a Supabase |
| `SUPABASE_ANON_KEY` | Settings → API → `anon` `public` | Chiave pubblica |
| `SUPABASE_SERVICE_KEY` | Settings → API → `service_role` (segreta) | Salvataggio partite (bypass RLS) |
| `SUPABASE_JWT_SECRET` | Settings → API → JWT Secret | Verifica locale dei token di login |

Dopo averle salvate, fai **redeploy** del backend.

## 2. Controlli su Supabase Auth

1. **Authentication → Providers → Email**  
   - Abilita Email  
   - Per i test: puoi disattivare “Confirm email” così la registrazione entra subito senza clic sulla mail

2. **Authentication → URL Configuration**  
   - Site URL = indirizzo del tuo sito (es. quello di Render)  
   - Se usi redirect, aggiungi l’URL del sito anche in Redirect URLs

3. **Tabelle**  
   - Le colonne `player0_uid`, `player1_uid`, `p1_is_ai` devono esistere su `games`  
   - Se non le hai ancora, esegui una volta `backend/supabase/migration_4_1.sql` nell’SQL Editor

## 3. Frontend

- Il file `backend/static/index.html` (v19) deve essere quello caricato  
- URL e anon key sono già dentro il file

## 4. Prova rapida (2 minuti)

1. Apri il sito  
2. Registrati con una email di prova (o accedi)  
3. Premi **Nuova vs IA**  
4. Se la partita parte → login + API ok  
5. Se compare un errore, copia il messaggio e segnalalo

## 5. Errori tipici

| Messaggio | Causa probabile | Cosa fare |
|-----------|-----------------|-----------|
| Auth non configurata / 503 | Mancano env su Render | Controlla punto 1 e redeploy |
| Token non valido / 401 | JWT secret sbagliato o sessione scaduta | Ricontrolla `SUPABASE_JWT_SECRET`, esci e rientra |
| 403 su partita | Non sei proprietario di quella partita | Crea una partita nuova da loggato |
| Registrazione non entra | “Confirm email” attivo | Disattivalo per i test (punto 2) |

## File di questa consegna

Solo documentazione (nessun codice nuovo da caricare).

## Prossimi possibili

- Migliorare messaggi di errore in interfaccia  
- Salvare meglio “chi sono in questa partita” (P0/P1)  
- Feature di gioco nuove  
