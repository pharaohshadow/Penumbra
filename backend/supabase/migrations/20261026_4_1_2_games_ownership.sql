-- Penumbra – 4.1.2 Migration: ownership su public.games
-- Applicare nell'SQL Editor di Supabase (o via CLI).
-- ADDITIVA e non distruttiva: colonne NULL, partite esistenti restano valide.

-- ---------------------------------------------------------------------------
-- 1) Colonne ownership
-- ---------------------------------------------------------------------------
alter table public.games
  add column if not exists player0_uid uuid null,
  add column if not exists player1_uid uuid null,
  add column if not exists vs_ai boolean not null default true;

comment on column public.games.player0_uid is 'Supabase auth.users.id dello slot 0 (umano in partita base)';
comment on column public.games.player1_uid is 'Supabase auth.users.id dello slot 1; NULL se vs_ai';
comment on column public.games.vs_ai is 'true = P1 è IA (partita base di test); false = PvP futuro';

-- FK opzionali verso auth.users (non bloccanti se uid assente)
-- Nota: su alcuni progetti serve lo schema auth esposto; se fallisce, commentare il blocco FK.
do $$
begin
  if not exists (
    select 1 from pg_constraint where conname = 'games_player0_uid_fkey'
  ) then
    alter table public.games
      add constraint games_player0_uid_fkey
      foreign key (player0_uid) references auth.users(id) on delete set null;
  end if;
  if not exists (
    select 1 from pg_constraint where conname = 'games_player1_uid_fkey'
  ) then
    alter table public.games
      add constraint games_player1_uid_fkey
      foreign key (player1_uid) references auth.users(id) on delete set null;
  end if;
exception
  when others then
    raise notice 'FK verso auth.users non aggiunte (ok in alcuni setup): %', sqlerrm;
end $$;

-- ---------------------------------------------------------------------------
-- 2) Indici (lookup membership in 4.2)
-- ---------------------------------------------------------------------------
create index if not exists games_player0_uid_idx on public.games (player0_uid)
  where player0_uid is not null;
create index if not exists games_player1_uid_idx on public.games (player1_uid)
  where player1_uid is not null;

-- ---------------------------------------------------------------------------
-- 3) Compatibilità backend attuale
-- ---------------------------------------------------------------------------
-- create_game / update_game NON inviano ancora queste colonne → restano default/null.
-- Nessun drop di policy qui (RLS aperta resta fino a 4.1.5).

-- Verifica rapida (opzionale):
-- select column_name, data_type, is_nullable, column_default
-- from information_schema.columns
-- where table_schema = 'public' and table_name = 'games'
-- order by ordinal_position;
