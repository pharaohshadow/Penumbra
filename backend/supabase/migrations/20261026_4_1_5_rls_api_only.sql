-- Penumbra – 4.1.5 RLS: niente accesso aperto anon alle tabelle di gioco
--
-- Decisione Fase 4: il BROWSER non interroga public.games / public.game_moves.
-- Solo l'API Render legge/scrive, con SUPABASE_SERVICE_KEY (service_role),
-- che BYPASSA la RLS.
--
-- Dopo questa migration:
--   - ruolo anon / authenticated via PostgREST diretto → nessun accesso utile alle partite
--   - backend con service_role → continua a funzionare come prima
--
-- PREREQUISITO Render: imposta SUPABASE_SERVICE_KEY (service_role) e preferiscila
-- rispetto alla sola ANON_KEY in supabase_store (vedi APPLY_4_1_5.md).

-- ---------------------------------------------------------------------------
-- 1) Rimuovi policy prototype "tutto aperto"
-- ---------------------------------------------------------------------------
drop policy if exists "games_anon_all" on public.games;
drop policy if exists "moves_anon_all" on public.game_moves;

-- ---------------------------------------------------------------------------
-- 2) RLS resta abilitata (già true dallo schema base)
-- ---------------------------------------------------------------------------
alter table public.games enable row level security;
alter table public.game_moves enable row level security;

-- ---------------------------------------------------------------------------
-- 3) Policy membership (opzionali, per futuri accessi authenticated diretti)
--    Non usate dal browser in Fase 4; utili se un giorno il client legge con JWT.
--    service_role ignora comunque queste policy.
-- ---------------------------------------------------------------------------

-- Lettura games solo se sei P0 o P1
drop policy if exists "games_select_members" on public.games;
create policy "games_select_members" on public.games
  for select
  to authenticated
  using (
    auth.uid() = player0_uid
    or auth.uid() = player1_uid
  );

-- Update solo membri
drop policy if exists "games_update_members" on public.games;
create policy "games_update_members" on public.games
  for update
  to authenticated
  using (
    auth.uid() = player0_uid
    or auth.uid() = player1_uid
  )
  with check (
    auth.uid() = player0_uid
    or auth.uid() = player1_uid
  );

-- Insert: solo autenticati, e player0_uid deve essere se stessi
drop policy if exists "games_insert_self_p0" on public.games;
create policy "games_insert_self_p0" on public.games
  for insert
  to authenticated
  with check (
    auth.uid() = player0_uid
  );

-- game_moves: solo se sei membro della partita
drop policy if exists "moves_select_members" on public.game_moves;
create policy "moves_select_members" on public.game_moves
  for select
  to authenticated
  using (
    exists (
      select 1 from public.games g
      where g.id = game_id
        and (g.player0_uid = auth.uid() or g.player1_uid = auth.uid())
    )
  );

drop policy if exists "moves_insert_members" on public.game_moves;
create policy "moves_insert_members" on public.game_moves
  for insert
  to authenticated
  with check (
    exists (
      select 1 from public.games g
      where g.id = game_id
        and (g.player0_uid = auth.uid() or g.player1_uid = auth.uid())
    )
  );

-- Nessuna policy per ruolo `anon` → anon non legge/scrive games/moves.

-- ---------------------------------------------------------------------------
-- 4) Verifica (esegui a mano dopo)
-- ---------------------------------------------------------------------------
-- select polname, tablename from pg_policies
-- where schemaname = 'public' and tablename in ('games', 'game_moves');
