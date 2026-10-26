# Come applicare 4.1.5 (RLS API-only)

## Perché

Le policy `games_anon_all` / `moves_anon_all` permettevano a chiunque con la **anon key** di leggere tutte le partite (anche spectator).  
In Fase 4: **solo i player del match**; il client non parla con le tabelle.

## Passi

### 1. Render – service role key

1. Supabase → **Settings → API** → copia `service_role` (**secret**)
2. Render → Environment:
   - `SUPABASE_URL` = già presente
   - `SUPABASE_SERVICE_KEY` = service_role  
   - (opzionale) lascia anche `SUPABASE_ANON_KEY` ma il backend deve preferire la service key

3. Redeploy dopo aver salvato la env.

`supabase_store.py` attuale fa già:

```text
SUPABASE_ANON_KEY or SUPABASE_SERVICE_KEY
```

Ordine consigliato in codice (4.2 o mini-patch sotto): **preferire SERVICE_KEY se presente**.  
Se oggi hai solo ANON_KEY e applichi questa RLS **senza** service key, create/fetch **smontano**.

### 2. SQL

SQL Editor → esegui:

`migrations/20261026_4_1_5_rls_api_only.sql`

### 3. Smoke rapido

- API Render: `GET /api/health` ok  
- Crea/riprendi una partita come prima (con service key)  
- Da Table Editor con ruolo anon non dovresti più listare tutto via API REST pubblica

## Mini-patch consigliata (opzionale in questo step)

In `supabase_store.py`, invertire la priorità della key:

```python
SUPABASE_KEY = (
    os.environ.get("SUPABASE_SERVICE_KEY", "")
    or os.environ.get("SUPABASE_ANON_KEY", "")
)
```

Così con entrambe le env vince la service role (bypass RLS).  
File patch incluso in questa consegna se vuoi applicarlo subito:  
`backend/api/supabase_store_key_priority.patch.md`

## Cosa non fa 4.1.5

- Non valida ancora il JWT del giocatore sugli endpoint (→ **4.2**)
- Non impedisce a chi ha la **service_role** di leggere tutto (è voluto per il server)
- Non crea utenti (già 4.1.4)

## Rollback di emergenza

Se qualcosa non torna, puoi ripristinare temporaneamente:

```sql
drop policy if exists "games_select_members" on public.games;
-- ... drop altre policy 4.1.5 ...
create policy "games_anon_all" on public.games for all using (true) with check (true);
create policy "moves_anon_all" on public.game_moves for all using (true) with check (true);
```

Poi sistema la service key e riapplica 4.1.5.
