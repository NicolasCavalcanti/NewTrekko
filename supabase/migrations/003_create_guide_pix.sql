-- guide_pix_keys: stores the mandatory Pix key required for guides to receive payments
create table if not exists guide_pix_keys (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  pix_key_type text not null check (pix_key_type in ('cpf', 'cnpj', 'email', 'phone', 'random')),
  pix_key_value text not null,
  pix_key_status text not null default 'pending' check (pix_key_status in ('pending', 'active', 'inactive')),
  pix_key_verified boolean not null default false,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  constraint guide_pix_keys_user_id_unique unique (user_id)
);

alter table guide_pix_keys enable row level security;

create policy if not exists "guide can view own pix key"
  on guide_pix_keys for select
  using (auth.uid() = user_id);

create policy if not exists "guide can insert own pix key"
  on guide_pix_keys for insert
  with check (auth.uid() = user_id);

create policy if not exists "guide can update own pix key"
  on guide_pix_keys for update
  using (auth.uid() = user_id);
