# Come applicare 4.1.2

## Se il progetto Supabase ha già lo schema vecchio

1. Apri **SQL Editor** nel dashboard Supabase
2. Incolla ed esegui il contenuto di:
   `migrations/20261026_4_1_2_games_ownership.sql`
3. Se il blocco FK verso `auth.users` dà errore, ignoralo (le colonne restano comunque)
4. Verifica:

```sql
select column_name, data_type, is_nullable, column_default
from information_schema.columns
where table_schema = 'public' and table_name = 'games'
  and column_name in ('player0_uid', 'player1_uid', 'vs_ai');
```

Atteso: tre righe, uid nullable, `vs_ai` default true.

## Se parti da zero

Esegui l’intero `schema.sql` aggiornato in questa cartella.

## Backend Render

- **Nessun redeploy obbligatorio** per 4.1.2: `supabase_store.py` non invia ancora le nuove colonne; restano default/null.
- Non rompe create/update/fetch esistenti.

## Non incluso in 4.1.2

- Auth utenti (4.1.3–4.1.4)
- Chiusura RLS (4.1.5)
- JWT sugli endpoint (4.2)
