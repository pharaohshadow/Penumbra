-- Migration 4.1 – da schema prototipo (anon open) a ownership + RLS players-only
-- Esegui nell'SQL Editor se hai già creato le tabelle con lo schema vecchio.

-- Colonne ownership
alter table public.games
  add column if not exists player0_uid uuid null references auth.users(id) on delete set null;

alter table public.games
  add column if not exists player1_uid uuid null references auth.users(id) on delete set null;

alter table public.games
  add column if not exists p1_is_ai boolean not null default true;

create index if not exists games_player0_uid_idx on public.games (player0_uid);
create index if not exists games_player1_uid_idx on public.games (player1_uid);

-- Sostituisci policy aperte
alter table public.games enable row level security;
alter table public.game_moves enable row level security;

drop policy if exists "games_anon_all" on public.games;
drop policy if exists "moves_anon_all" on public.game_moves;
drop policy if exists "games_select_players" on public.games;
drop policy if exists "games_insert_auth" on public.games;
drop policy if exists "games_update_players" on public.games;
drop policy if exists "moves_select_players" on public.game_moves;
drop policy if exists "moves_insert_players" on public.game_moves;

create policy "games_select_players" on public.games
  for select
  using (
    auth.uid() is not null
    and (auth.uid() = player0_uid or auth.uid() = player1_uid)
  );

create policy "games_insert_auth" on public.games
  for insert
  with check (
    auth.uid() is not null
    and auth.uid() = player0_uid
  );

create policy "games_update_players" on public.games
  for update
  using (
    auth.uid() is not null
    and (auth.uid() = player0_uid or auth.uid() = player1_uid)
  )
  with check (
    auth.uid() is not null
    and (auth.uid() = player0_uid or auth.uid() = player1_uid)
  );

create policy "moves_select_players" on public.game_moves
  for select
  using (
    exists (
      select 1 from public.games g
      where g.id = game_id
        and auth.uid() is not null
        and (auth.uid() = g.player0_uid or auth.uid() = g.player1_uid)
    )
  );

create policy "moves_insert_players" on public.game_moves
  for insert
  with check (
    exists (
      select 1 from public.games g
      where g.id = game_id
        and auth.uid() is not null
        and (auth.uid() = g.player0_uid or auth.uid() = g.player1_uid)
    )
  );

-- Partite vecchie senza uid restano inaccessibili via RLS client:
-- o le assegni manualmente, o le usi solo via service_role backend.
