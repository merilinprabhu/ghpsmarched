-- ==============================================================================
-- SAFE FIX FOR SUPABASE STORAGE & DATABASE POLICIES
-- (Removed "ALTER TABLE storage.objects" to prevent ERROR 42501)
-- ==============================================================================

-- 1. Create or ensure 'school-logo' bucket is PUBLIC
INSERT INTO storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
VALUES (
    'school-logo',
    'school-logo',
    true,
    5242880,
    ARRAY['image/png', 'image/jpeg', 'image/jpg', 'image/svg+xml', 'image/webp', 'image/gif']
)
ON CONFLICT (id) DO UPDATE SET 
    public = true,
    file_size_limit = 5242880,
    allowed_mime_types = ARRAY['image/png', 'image/jpeg', 'image/jpg', 'image/svg+xml', 'image/webp', 'image/gif'];

-- 2. Drop any previous policies on storage.objects for this bucket
DROP POLICY IF EXISTS "Allow public read school-logo" ON storage.objects;
DROP POLICY IF EXISTS "Allow public insert school-logo" ON storage.objects;
DROP POLICY IF EXISTS "Allow public update school-logo" ON storage.objects;
DROP POLICY IF EXISTS "Allow public delete school-logo" ON storage.objects;
DROP POLICY IF EXISTS "Public Access school-logo" ON storage.objects;
DROP POLICY IF EXISTS "Allow authenticated uploads school-logo" ON storage.objects;

-- 3. Create Storage Policies for 'school-logo' bucket
CREATE POLICY "Allow public read school-logo"
ON storage.objects FOR SELECT
TO public
USING (bucket_id = 'school-logo');

CREATE POLICY "Allow public insert school-logo"
ON storage.objects FOR INSERT
TO public
WITH CHECK (bucket_id = 'school-logo');

CREATE POLICY "Allow public update school-logo"
ON storage.objects FOR UPDATE
TO public
USING (bucket_id = 'school-logo')
WITH CHECK (bucket_id = 'school-logo');

CREATE POLICY "Allow public delete school-logo"
ON storage.objects FOR DELETE
TO public
USING (bucket_id = 'school-logo');

-- 4. Ensure school_settings table exists and has open RLS
CREATE TABLE IF NOT EXISTS public.school_settings (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id UUID NOT NULL,
    settings_key TEXT NOT NULL,
    settings_value JSONB NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

ALTER TABLE public.school_settings ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow all access to school_settings" ON public.school_settings;
CREATE POLICY "Allow all access to school_settings"
ON public.school_settings FOR ALL
TO public
USING (true)
WITH CHECK (true);

-- 5. Ensure schools table has open RLS
ALTER TABLE public.schools ENABLE ROW LEVEL SECURITY;

DROP POLICY IF EXISTS "Allow all access to schools" ON public.schools;
CREATE POLICY "Allow all access to schools"
ON public.schools FOR ALL
TO public
USING (true)
WITH CHECK (true);
