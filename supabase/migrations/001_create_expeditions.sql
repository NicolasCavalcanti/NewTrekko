-- Expeditions table for guide-created trips visible to all users
create table if not exists expeditions (
  id bigserial primary key,
  guide_id text not null,
  guide_name text,
  trail_id integer not null,
  trail_name text,
  title text,
  start_date timestamptz not null,
  end_date timestamptz,
  capacity integer not null default 10,
  available_spots integer not null default 10,
  price text,
  meeting_point text,
  notes text,
  status text not null default 'active',
  created_at timestamptz default now()
);

-- Enable Row Level Security
alter table expeditions enable row level security;

-- Anyone can read non-cancelled expeditions
create policy if not exists "Public can read active expeditions"
  on expeditions for select
  using (status != 'cancelled');

-- Authenticated guides can insert their own expeditions
create policy if not exists "Guides can insert own expeditions"
  on expeditions for insert
  with check (auth.uid()::text = guide_id);

-- Guides can delete their own expeditions
create policy if not exists "Guides can delete own expeditions"
  on expeditions for delete
  using (auth.uid()::text = guide_id);
