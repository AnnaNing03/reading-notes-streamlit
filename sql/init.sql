-- =============================================
-- 读书笔记应用 - 数据库初始化脚本
-- =============================================

-- 1. 创建 notes 表
create table if not exists public.notes (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  book_name text not null,
  sentence text not null,
  thought text not null,
  date date not null default current_date,
  created_at timestamptz not null default now()
);

-- 2. 启用行级安全（RLS）
alter table public.notes enable row level security;

-- 3. 创建 RLS 策略：用户只能操作自己的数据

-- 查询策略
create policy "Users can read own notes"
  on public.notes for select
  using (auth.uid() = user_id);

-- 插入策略
create policy "Users can insert own notes"
  on public.notes for insert
  with check (auth.uid() = user_id);

-- 更新策略
create policy "Users can update own notes"
  on public.notes for update
  using (auth.uid() = user_id)
  with check (auth.uid() = user_id);

-- 删除策略
create policy "Users can delete own notes"
  on public.notes for delete
  using (auth.uid() = user_id);

-- 4. 创建索引以加速查询
create index if not exists idx_notes_user_id on public.notes(user_id);
create index if not exists idx_notes_user_book on public.notes(user_id, book_name);
create index if not exists idx_notes_user_date on public.notes(user_id, date desc);
