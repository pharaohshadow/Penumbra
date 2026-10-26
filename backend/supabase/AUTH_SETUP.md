# Auth setup – Penumbra 4.1

## 1. Abilita Email Auth in Supabase

Dashboard → **Authentication** → **Providers** → Email → Enabled.

Per email fittizie in sviluppo (`fra@test.local`):

- **Authentication → Settings**
  - Disabilita “Confirm email” in dev (o conferma manualmente gli utenti)
  - Eventualmente abilita “Allow unrestricted email domains” se presente, oppure crea gli utenti da Admin

Le email `*@test.local` non ricevono posta reale: crea gli utenti da **Authentication → Users → Add user** (auto-confirm).

## 2. Utenti di test consigliati

Crea almeno due utenti (Add user, password a scelta, auto-confirm):

| Email            | Ruolo test        |
|------------------|-------------------|
| `fra@test.local` | Player 0 / host   |
| `ai@test.local`  | Riserva / P1 umano futuro |

Salva i **UUID** mostrati in dashboard (servono per assegnare `player0_uid` / `player1_uid`).

## 3. Esegui lo schema

SQL Editor → incolla ed esegui `schema.sql` di questa consegna (v5).

Verifica colonne:

```sql
select column_name from information_schema.columns
where table_schema = 'public' and table_name = 'games'
order by 1;
```

Devono comparire `player0_uid`, `player1_uid`, `turn_deadline_at`.

## 4. Chiavi progetto

Dashboard → **Settings → API**:

| Variabile Render / env     | Quale chiave                          | Uso |
|----------------------------|----------------------------------------|-----|
| `SUPABASE_URL`             | Project URL                            | API |
| `SUPABASE_ANON_KEY`        | `anon` `public`                        | Client login + (opz.) verify user |
| `SUPABASE_SERVICE_KEY`     | `service_role` **secret**              | Solo backend: bypass RLS, write games |

**Non** esporre `service_role` nel frontend o su GitHub Pages.

## 5. Test manuale ownership

Dopo aver creato un utente e copiato il suo uid:

```sql
-- Esempio: assegna una partita esistente a fra@test.local
update public.games
set player0_uid = 'UUID-DI-FRA'
where id = 'UUID-PARTITA';
```

Con JWT di `fra@test.local`, una select REST su quella riga deve funzionare; con un altro utente → 0 righe / 401.

## 6. Done 4.1

- [ ] Schema eseguito
- [ ] Due utenti `*@test.local` creati (auto-confirm)
- [ ] Almeno una riga `games` con `player0_uid` impostato
- [ ] Env Render aggiornate con `SUPABASE_SERVICE_KEY` (oltre URL + anon)
