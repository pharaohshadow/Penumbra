# 4.1.1 – Inventario schema Supabase (as-is vs to-be)

**Data inventario:** 2026-10-26  
**Fonte:** `backend/supabase/schema.sql` + uso in `backend/api/supabase_store.py`  
**Stato:** solo documentazione; nessuna migration applicata in questo step.

---

## As-is

### Tabella `public.games`

| Colonna | Tipo | Note |
|---------|------|------|
| `id` | uuid PK | default `gen_random_uuid()`; API può impostarlo dal client |
| `created_at` | timestamptz | default now() |
| `updated_at` | timestamptz | aggiornato da `update_game` |
| `status` | text | `active` \| `finished` \| `abandoned` |
| `turn` | int | denormalizzato dallo state |
| `phase` | text | es. MAIN, DRAFT |
| `current_player` | int | 0 / 1 |
| `winner` | int null | |
| `main_quest` | text null | |
| `state_json` | jsonb | snapshot completo API (board, players, draft_full, …) |

**Indici:** `games_status_idx`, `games_updated_at_idx`

**Manca per ownership / auth:**
- nessun `player0_uid` / `player1_uid`
- nessun flag `vs_ai`
- nessun legame a `auth.users`

### Tabella `public.game_moves`

| Colonna | Tipo | Note |
|---------|------|------|
| `id` | bigserial PK | |
| `game_id` | uuid FK → games | on delete cascade |
| `created_at` | timestamptz | |
| `player_id` | int | 0/1 di gioco, **non** uid Supabase |
| `action` | text | move, play, end_turn, … |
| `payload` | jsonb | |

**Indice:** `game_moves_game_id_idx`

### RLS attuale

- RLS **abilitato** su `games` e `game_moves`
- Policy `games_anon_all` / `moves_anon_all`: **for all using (true) with check (true)**  
  → di fatto accesso aperto a chi ha la anon key (prototipo)

### Come scrive il backend oggi (`supabase_store.py`)

- Env: `SUPABASE_URL` + `SUPABASE_ANON_KEY` (o `SUPABASE_SERVICE_KEY`)
- `create_game`: insert su colonne sopra + `state_json` (niente uid)
- `update_game` / `fetch_game` / `log_move`: idem
- Nessuna verifica JWT giocatore

### File presenti in repo

- Solo `backend/supabase/schema.sql` (nessuna migration versionata)

---

## To-be (scelta per partita base Fase 4)

### Ownership (preferenza confermata)

**Colonne su `games`** (non tabella `game_members`):

| Colonna | Tipo | Significato |
|---------|------|-------------|
| `player0_uid` | uuid null | Supabase Auth uid del giocatore slot 0 (umano in partita base) |
| `player1_uid` | uuid null | uid slot 1; **null** se vs IA |
| `vs_ai` | boolean not null default true | partita base vs IA |

- Partite **legacy**: uid null → comportamento attuale fino a 4.2 (API ancora aperta o solo restore).
- Partite **nuove** (dopo 4.2): `player0_uid` obbligatorio a create; `player1_uid` null se `vs_ai`.

### Accesso dati (decisione Fase 4)

- Il **browser non** interroga `games` / `game_moves` direttamente.
- Solo l’**API Render** legge/scrive tabelle (chiave server).
- RLS verrà stretta in 4.1.5 (togliere policy anon all-open); il server userà service role o policy dedicate.

### Auth

- Email/password Supabase; utenti test `*@test.local` creati da dashboard (4.1.3–4.1.4).
- JWT validato in **4.2**, non in 4.1.

### Cosa non si tocca in 4.1

- Forma di `state_json` (già v22: tile, status, draft_full)
- Motore di gioco / endpoint pubblici esistenti (nessun breaking fino a 4.2)

---

## Impatto su `supabase_store.py` (preview, non implementato qui)

Dopo 4.1.2 + 4.2:

- `create_game(..., player0_uid=..., player1_uid=None, vs_ai=True)`
- `fetch_game` può restituire anche gli uid per check membership lato API
- Colonne nuove **nullable** → create/update attuali restano validi se non inviano uid

---

## Prossimo micro-step

**4.1.2** – file migration SQL additivo (`player0_uid`, `player1_uid`, `vs_ai` + indici + commenti applicazione).
