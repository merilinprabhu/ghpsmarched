-- Migration to create school_settings table for persisting school-wise configurations
CREATE TABLE IF NOT EXISTS public.school_settings (
  school_id uuid REFERENCES public.schools(id) ON DELETE CASCADE,
  settings_key text NOT NULL,
  settings_value jsonb NOT NULL DEFAULT '{}'::jsonb,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
  updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
  PRIMARY KEY (school_id, settings_key)
);

-- Enable RLS for school_settings
ALTER TABLE public.school_settings ENABLE ROW LEVEL SECURITY;

-- Policies for school_settings
DROP POLICY IF EXISTS "Allow select settings for same school" ON public.school_settings;
CREATE POLICY "Allow select settings for same school" ON public.school_settings
  FOR SELECT TO authenticated
  USING (
    school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid())
    OR (SELECT role FROM public.profiles WHERE id = auth.uid()) = 'developer'
  );

DROP POLICY IF EXISTS "Allow insert settings for same school" ON public.school_settings;
CREATE POLICY "Allow insert settings for same school" ON public.school_settings
  FOR INSERT TO authenticated
  WITH CHECK (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));

DROP POLICY IF EXISTS "Allow update settings for same school" ON public.school_settings;
CREATE POLICY "Allow update settings for same school" ON public.school_settings
  FOR UPDATE TO authenticated
  USING (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));

DROP POLICY IF EXISTS "Allow delete settings for same school" ON public.school_settings;
CREATE POLICY "Allow delete settings for same school" ON public.school_settings
  FOR DELETE TO authenticated
  USING (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));
