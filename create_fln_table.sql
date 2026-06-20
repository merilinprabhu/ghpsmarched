-- Migration to create fln_evaluations table for FLN Assessment

CREATE TABLE IF NOT EXISTS public.fln_evaluations (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  school_id uuid REFERENCES public.schools(id) ON DELETE CASCADE,
  student_id uuid REFERENCES public.admissions(id) ON DELETE CASCADE,
  class_name text NOT NULL,
  evaluation_date date NOT NULL DEFAULT CURRENT_DATE,
  outcomes jsonb NOT NULL DEFAULT '{}'::jsonb, -- {col_1: 'BB', ..., col_17: 'A'}
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
  updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
  UNIQUE(student_id, evaluation_date)
);

-- Enable RLS for fln_evaluations
ALTER TABLE public.fln_evaluations ENABLE ROW LEVEL SECURITY;

-- Policies for fln_evaluations
DROP POLICY IF EXISTS "Allow select fln for same school users" ON public.fln_evaluations;
CREATE POLICY "Allow select fln for same school users" ON public.fln_evaluations
  FOR SELECT TO authenticated
  USING (
    school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid())
    OR (SELECT role FROM public.profiles WHERE id = auth.uid()) = 'developer'
  );

DROP POLICY IF EXISTS "Allow insert fln for same school users" ON public.fln_evaluations;
CREATE POLICY "Allow insert fln for same school users" ON public.fln_evaluations
  FOR INSERT TO authenticated
  WITH CHECK (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));

DROP POLICY IF EXISTS "Allow update fln for same school users" ON public.fln_evaluations;
CREATE POLICY "Allow update fln for same school users" ON public.fln_evaluations
  FOR UPDATE TO authenticated
  USING (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));

DROP POLICY IF EXISTS "Allow delete fln for same school users" ON public.fln_evaluations;
CREATE POLICY "Allow delete fln for same school users" ON public.fln_evaluations
  FOR DELETE TO authenticated
  USING (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));
