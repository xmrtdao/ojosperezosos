-- OjosPerezosos Supabase Schema
-- Accessibility-focused multimodal AI — AMD Developer Hackathon

-- Scene descriptions cache
create table if not exists descriptions (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references auth.users(id) on delete cascade,
    image_hash text not null,
    caption text not null,
    detail_level text default 'standard',
    created_at timestamptz default now()
);

-- OCR text cache
create table if not exists ocr_cache (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references auth.users(id) on delete cascade,
    image_hash text not null,
    full_text text not null,
    lines jsonb default '[]',
    created_at timestamptz default now()
);

-- User preferences (accessibility settings)
create table if not exists user_prefs (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references auth.users(id) on delete cascade,
    voice text default 'default',
    speech_rate numeric default 1.0,
    detail_level text default 'standard',
    preferred_language text default 'en',
    created_at timestamptz default now(),
    updated_at timestamptz default now()
);

-- TTS audio cache (shared, since audio is non-sensitive)
create table if not exists tts_cache (
    id uuid primary key default gen_random_uuid(),
    text_hash text unique not null,
    text_content text not null,
    audio_url text not null,
    voice text default 'default',
    created_at timestamptz default now()
);

-- Object detection history
create table if not exists object_scans (
    id uuid primary key default gen_random_uuid(),
    user_id uuid references auth.users(id) on delete cascade,
    image_hash text,
    query text,
    results jsonb not null default '[]',
    created_at timestamptz default now()
);

-- Enable RLS
alter table descriptions enable row level security;
alter table ocr_cache enable row level security;
alter table user_prefs enable row level security;
alter table tts_cache enable row level security;
alter table object_scans enable row level security;

-- RLS policies
 create policy "Users own descriptions"
    on descriptions for all using (user_id = auth.uid());

 create policy "Users own OCR cache"
    on ocr_cache for all using (user_id = auth.uid());

 create policy "Users own preferences"
    on user_prefs for all using (user_id = auth.uid());

 create policy "TTS public read"
    on tts_cache for select to anon, authenticated using (true);

 create policy "Users own object scans"
    on object_scans for all using (user_id = auth.uid());

-- Indexes
 create index idx_desc_user on descriptions(user_id);
 create index idx_desc_hash on descriptions(image_hash);
 create index idx_ocr_user on ocr_cache(user_id);
 create index idx_ocr_hash on ocr_cache(image_hash);
 create index idx_obj_user on object_scans(user_id);
 create index idx_obj_created on object_scans(created_at desc);
