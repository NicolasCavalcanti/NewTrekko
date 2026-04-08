-- Enrollments table — tracks which users enrolled in which expeditions
create table if not exists enrollments (
  id bigserial primary key,
  expedition_id bigint not null references expeditions(id) on delete cascade,
  user_id text not null,
  user_name text,
  user_email text,
  spots integer not null default 1,
  status text not null default 'confirmed',  -- confirmed | pending_payment | cancelled
  created_at timestamptz default now(),
  unique(expedition_id, user_id)
);

alter table enrollments enable row level security;

-- Users can see their own enrollments
create policy if not exists "Users can read own enrollments"
  on enrollments for select
  using (auth.uid()::text = user_id);

-- Guides can see enrollments for their expeditions
create policy if not exists "Guides can read expedition enrollments"
  on enrollments for select
  using (
    exists (
      select 1 from expeditions
      where expeditions.id = enrollments.expedition_id
        and expeditions.guide_id = auth.uid()::text
    )
  );

-- Users can enroll themselves
create policy if not exists "Users can insert own enrollments"
  on enrollments for insert
  with check (auth.uid()::text = user_id);

-- Users can update their own enrollment (e.g. cancel)
create policy if not exists "Users can update own enrollments"
  on enrollments for update
  using (auth.uid()::text = user_id);

-- Users can delete their own enrollment
create policy if not exists "Users can delete own enrollments"
  on enrollments for delete
  using (auth.uid()::text = user_id);

-- Function: enroll_in_expedition — atomically inserts enrollment and decrements available_spots
create or replace function enroll_in_expedition(
  p_expedition_id bigint,
  p_user_id text,
  p_user_name text,
  p_user_email text,
  p_spots integer
) returns jsonb
language plpgsql
security definer
as $$
declare
  v_spots integer;
  v_result jsonb;
begin
  -- Lock the expedition row
  select available_spots into v_spots
    from expeditions
   where id = p_expedition_id
     and status != 'cancelled'
     for update;

  if not found then
    return jsonb_build_object('success', false, 'error', 'Expedição não encontrada ou cancelada');
  end if;

  if v_spots < p_spots then
    return jsonb_build_object('success', false, 'error', 'Vagas insuficientes');
  end if;

  -- Insert enrollment (unique constraint handles duplicates)
  insert into enrollments(expedition_id, user_id, user_name, user_email, spots, status)
    values (p_expedition_id, p_user_id, p_user_name, p_user_email, p_spots, 'confirmed')
    on conflict (expedition_id, user_id) do update
      set status = 'confirmed', spots = p_spots;

  -- Decrement available spots
  update expeditions
     set available_spots = available_spots - p_spots
   where id = p_expedition_id;

  return jsonb_build_object('success', true, 'error', null);
exception when others then
  return jsonb_build_object('success', false, 'error', sqlerrm);
end;
$$;

-- Function: cancel_enrollment — atomically removes enrollment and restores available_spots
create or replace function cancel_enrollment(
  p_expedition_id bigint,
  p_user_id text
) returns jsonb
language plpgsql
security definer
as $$
declare
  v_spots integer;
begin
  select spots into v_spots
    from enrollments
   where expedition_id = p_expedition_id
     and user_id = p_user_id
     and status != 'cancelled';

  if not found then
    return jsonb_build_object('success', false, 'error', 'Inscrição não encontrada');
  end if;

  delete from enrollments
   where expedition_id = p_expedition_id
     and user_id = p_user_id;

  update expeditions
     set available_spots = least(capacity, available_spots + v_spots)
   where id = p_expedition_id;

  return jsonb_build_object('success', true, 'error', null);
exception when others then
  return jsonb_build_object('success', false, 'error', sqlerrm);
end;
$$;
