# 4.1.6 – Smoke test manuale (chiusura blocco 4.1)

Esegui nell’ordine. Segna le caselle.  
Se un punto fallisce, ferma e correggi prima di passare a **4.2**.

---

## 0. Prerequisiti

- [ ] Migration **4.1.2** applicata (`player0_uid`, `player1_uid`, `vs_ai` presenti)
- [ ] Auth **4.1.3** ok (Email provider, confirm off in dev)
- [ ] User test **4.1.4** creato (`fra@test.local` + UID annotato in privato)
- [ ] RLS **4.1.5** applicata + `SUPABASE_SERVICE_KEY` su Render
- [ ] `supabase_store.py` con priorità SERVICE_KEY deployato
- [ ] URL API Render noto (es. `https://penumbra-backend.onrender.com`)

---

## 1. Health API

```bash
curl -sS "https://TUO-URL-RENDER/api/health"
```

- [ ] Risposta JSON con `"ok": true`
- [ ] `"supabase": true` (se le env sono impostate)
- [ ] Versione presente (es. 0.22 o successiva)

Se `supabase: false` → manca URL o key su Render.

---

## 2. Legacy: partita senza ownership (uid null)

Simula il flusso pre-auth (ancora usato finché 4.2 non obbliga il JWT).

```bash
# Nuova partita vs IA
curl -sS -X POST "https://TUO-URL-RENDER/api/new" \
  -H "Content-Type: application/json" \
  -d '{"vs_ai": true, "name": "SmokeTest"}'
```

- [ ] Ritorna `game_id` e `board`
- [ ] Annota `GAME_ID=...`

```bash
curl -sS "https://TUO-URL-RENDER/api/state?game_id=GAME_ID"
```

- [ ] Stesso stato / partita trovata (memoria o Supabase)

In SQL Editor:

```sql
select id, player0_uid, player1_uid, vs_ai, status, turn
from public.games
where id = 'GAME_ID';
```

- [ ] Riga presente (se persistenza attiva)
- [ ] `player0_uid` / `player1_uid` ancora **null** è accettabile pre-4.2
- [ ] `vs_ai` default true se colonna valorizzata dal DB

---

## 3. Ownership: assegna uid di test

```sql
update public.games
set
  player0_uid = 'IL_TUO_TEST_USER_UID'::uuid,
  player1_uid = null,
  vs_ai = true
where id = 'GAME_ID'::uuid;

select id, player0_uid, vs_ai from public.games where id = 'GAME_ID'::uuid;
```

- [ ] Update ok
- [ ] `player0_uid` = uid di `fra@test.local`

---

## 4. Restore dopo “forget” memoria

L’API tiene le partite in RAM; dopo restart/sleep deve rileggerle da Supabase.

Opzioni:
- Attendi sleep Render, **oppure**
- Redeploy Render, **oppure**
- Se puoi, restart del servizio

Poi:

```bash
curl -sS "https://TUO-URL-RENDER/api/state?game_id=GAME_ID"
```

- [ ] Partita **non** 404
- [ ] Board/log coerenti (hydrate ok)
- [ ] Eventuale log tipo “ripristinata da Supabase” se esposto

---

## 5. RLS: anon non deve listare tutto

Con **solo** anon key (non service), da SQL non è banale; verifica concettuale:

- [ ] Policy `games_anon_all` **assente** (`pg_policies` / dashboard Auth policies)
- [ ] Esistono policy `games_select_members` (o nomi equivalenti 4.1.5)

```sql
select tablename, policyname
from pg_policies
where schemaname = 'public'
  and tablename in ('games', 'game_moves')
order by tablename, policyname;
```

- [ ] Niente policy “for all using (true)” sulle due tabelle
- [ ] Presenti policy members

---

## 6. Service key backend

- [ ] Su Render c’è `SUPABASE_SERVICE_KEY`
- [ ] Dopo RLS, create/update/fetch via API funzionano ancora (punto 2 e 4)

Se 2 fallisce con errori Supabase nei log Render → key sbagliata o SQL RLS applicato senza service key.

---

## 7. Regressione motore (minima)

```bash
# end turn (se in MAIN e tocca P0)
curl -sS -X POST "https://TUO-URL-RENDER/api/end" \
  -H "Content-Type: application/json" \
  -d '{"game_id":"GAME_ID","player_id":0}'
```

- [ ] 200 o errore di regole di gioco coerente (non 500 generico)
- [ ] Nessun traceback inatteso nei log Render

---

## Esito

| Area | Ok? |
|------|-----|
| Health + supabase enabled | |
| New/state legacy | |
| Ownership SQL | |
| Restore post-sleep/redeploy | |
| RLS senza anon-open | |
| Service key | |
| Azione di gioco base | |

**4.1.6 done** quando tutte le righe rilevanti sono ok (o accettate come limitazione documentata).

---

## Limitazioni note (non bloccanti per chiudere 4.1)

- API **non** verifica ancora JWT / membership (→ **4.2**): chiunque con `game_id` può ancora chiamare gli endpoint
- UI login non esiste (→ **4.4**)
- Timer turno non c’è (→ **4.3**)

Chiudere 4.1 = **schema + auth config + RLS server-side** pronti per agganciare JWT in 4.2.
