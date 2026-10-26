# Smoke test 4.2.7 – prove rapide (in parole semplici)

Queste sono le prove minime per capire se la protezione funziona.  
Non serve essere programmatori: basta avere due account di test su Supabase e un modo per chiamare l’API (browser, Postman, oppure la UI se già manda il token).

## Cosa ti serve

1. Due utenti di test su Supabase (es. utente A e utente B)
2. Il token di accesso (JWT) di ciascuno dopo il login
3. L’indirizzo del backend (es. su Render)

## Prove da fare

### 1. Health (deve funzionare senza login)
- Chiama `GET /api/health`
- Aspettati: risposta ok, senza errori

### 2. Creare partita senza essere loggati
- Chiama `POST /api/new` **senza** token
- Aspettati: errore **401**

### 3. Creare partita da loggati (utente A)
- Chiama `POST /api/new` **con** il token di A
- Aspettati: partita creata, con A come proprietario
- Annotati il `game_id` che ti restituisce

### 4. Vedere la partita da un estraneo (utente B)
- Chiama `GET /api/state?game_id=...` con il token di B
- Aspettati: errore **403** (non è un giocatore di quella partita)

### 5. Vedere la partita dal proprietario (utente A)
- Stessa chiamata con il token di A
- Aspettati: stato della partita ok

### 6. Unirsi a una partita vs IA
- Crea una partita con `vs_ai: true`
- Prova a fare join con utente B
- Aspettati: errore **400** (non si può joinare partite vs IA)

### 7. Unirsi a una partita PvP
- Crea una partita con `vs_ai: false` (utente A)
- Fai join con utente B (loggato)
- Aspettati: ok, B diventa secondo giocatore
- Ora sia A che B devono poter vedere/giocare
- Un terzo utente deve ricevere **403**

### 8. Unirsi alla propria partita
- Utente A prova a fare join sulla partita che ha creato
- Aspettati: errore **400**

### 9. Azioni di gioco senza token
- Qualsiasi mossa (`/api/move`, `/api/play`, ecc.) senza token
- Aspettati: **401**

### 10. Azioni di gioco da non-membro
- Utente estraneo prova a muovere su una partita altrui
- Aspettati: **403**

## Esito

Se tutte le prove sopra danno il risultato atteso → **4.2 è ok**.

Se qualcosa non torna, annota quale punto fallisce e si interviene lì.
