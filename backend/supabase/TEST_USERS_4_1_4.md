# 4.1.4 – Utenti di test Supabase

**Obiettivo:** almeno un account umano di test usabile come `player0_uid` nelle partite base.  
**Prerequisiti:** 4.1.3 (Email provider ON, confirm email off in dev).

---

## A. Creare l’utente (Dashboard – metodo consigliato)

1. Supabase → **Authentication** → **Users**
2. **Add user** → **Create new user**
3. Compila:
   - **Email:** `fra@test.local`
   - **Password:** scegline una (solo password manager; **mai** nel repo)
   - Spunta **Auto Confirm User** se disponibile (equivalente a user già confermato)
4. Conferma creazione
5. Apri la riga utente e **copia lo User UID** (uuid tipo `a1b2c3d4-...`)

### Utente opzionale (solo se vuoi sperimentare due umani più avanti)

| Email | Ruolo previsto |
|-------|----------------|
| `fra@test.local` | P0 – obbligatorio partita base |
| `p2@test.local` | P1 umano futuro (ora non serve per vs IA) |

Per la **partita base vs IA** basta **solo** `fra@test.local`.

---

## B. Verifica

- [ ] L’utente compare in Authentication → Users
- [ ] Non è banned / disabled
- [ ] UID copiato correttamente (36 caratteri con trattini)

---

## C. Dove annotare (PRIVATO – non git)

Crea in locale un file **fuori dal repo** oppure un secret manager, es.:

```text
# penumbra-secrets.local (NON committare)
SUPABASE_URL=https://xxxx.supabase.co
TEST_USER_EMAIL=fra@test.local
TEST_USER_UID=xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
TEST_USER_PASSWORD=********
```

In Render env **non** serve la password del test user (serve solo in browser al login in 4.4).  
In 4.1.6 / 4.2 userai l’**UID** per assegnare `player0_uid` a una riga `games`.

Template vuoto nel repo (senza secret): vedi `test_users.example.env`.

---

## D. Assegnazione di prova su una partita (opzionale ora, utile in 4.1.6)

Se hai già una riga in `games` e vuoi legarla all’uid:

```sql
-- Sostituisci i placeholder
update public.games
set
  player0_uid = 'TEST_USER_UID_QUI'::uuid,
  player1_uid = null,
  vs_ai = true
where id = 'GAME_ID_QUI'::uuid;
```

Controllo:

```sql
select id, player0_uid, player1_uid, vs_ai, status
from public.games
where player0_uid is not null
limit 5;
```

---

## E. Cosa non fare

- Non mettere password o UID “di produzione” nei commit
- Non usare la **service_role** key nel frontend
- Non creare utenti via signup pubblico se confirm email è ancora confuso: usa **Add user** in dashboard
- Non serve un secondo utente per chiudere 4.1.4

---

## Done 4.1.4

- [x] Procedura documentata  
- [ ] **Tu:** creato `fra@test.local` + UID annotato in privato  

Quando l’UID è salvato da te, 4.1.4 è operativamente completo.
