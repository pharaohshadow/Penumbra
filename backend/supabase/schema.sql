-- Penumbra – schema Supabase (baseline + ownership 4.1.2)
-- Per progetti NUOVI puoi eseguire questo file intero.
-- Per progetti già con lo schema v9: esegui solo migrations/20261026_4_1_2_games_ownership.sql

-- Partite
create table if not exists public.games (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  status text not null default 'active' check (status in ('active', 'finished', 'abandoned')),
  turn int not null default 1,
  phase text not null default 'MAIN',
  current_player int not null default 0,
  winner int null,
  main_quest text null,
  state_json jsonb not null default '{}'::jsonb,
  -- ownership (4.1.2)
  player0_uid uuid null,
  player1_uid uuid null,
  vs_ai boolean not null default true
);

create index if not exists games_status_idx on public.games (status);
create index if not exists games_updated_at_idx on public.games (updated_at desc);
create index if not exists games_player0_uid_idx on public.games (player0_uid)
  where player0_uid is not null;
create index if not exists games_player1_uid_idx on public.games (player1_uid)
  where player1_uid is not null;

-- Log mosse
create table if not exists public.game_moves (
  id bigserial primary key,
  game_id uuid not null references public.games(id) on delete cascade,
  created_at timestamptz not null default now(),
  player_id int not null,
  action text not null,
  payload jsonb not null default '{}'::jsonb
);

create index if not exists game_moves_game_id_idx on public.game_moves (game_id);

-- RLS: ancora aperta (prototipo). Stretta in 4.1.5.
alter table public.games enable row level security;
alter table public.game_moves enable row level security;

drop policy if exists "games_anon_all" on public.games;
create policy "games_anon_all" on public.games
  for all using (true) with check (true);

drop policy if exists "moves_anon_all" on public.game_moves;
create policy "moves_anon_all" on public.game_moves
  for all using (true) with check (true);

-- Realtime (opzionale): Database → Replication → games
