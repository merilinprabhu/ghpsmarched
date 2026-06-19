-- Migration to create database tables for academics: Bridge Course, CCE Assessment, and LBA Assessment

-- 1. Create public.bridge_course_evaluations table
CREATE TABLE IF NOT EXISTS public.bridge_course_evaluations (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  school_id uuid REFERENCES public.schools(id) ON DELETE CASCADE,
  student_id uuid REFERENCES public.admissions(id) ON DELETE CASCADE,
  class_name text NOT NULL,
  subject_name text NOT NULL,
  test_type text NOT NULL, -- PRE_TEST or POST_TEST
  competencies jsonb NOT NULL DEFAULT '{}'::jsonb, -- {c1: 'A'/'B', ..., c10: 'A'/'B'}
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
  updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
  UNIQUE(student_id, subject_name, test_type)
);

-- Enable RLS for bridge_course_evaluations
ALTER TABLE public.bridge_course_evaluations ENABLE ROW LEVEL SECURITY;

-- Policies for bridge_course_evaluations
DROP POLICY IF EXISTS "Allow select for same school users" ON public.bridge_course_evaluations;
CREATE POLICY "Allow select for same school users" ON public.bridge_course_evaluations
  FOR SELECT TO authenticated
  USING (
    school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid())
    OR (SELECT role FROM public.profiles WHERE id = auth.uid()) = 'developer'
  );

DROP POLICY IF EXISTS "Allow insert for same school users" ON public.bridge_course_evaluations;
CREATE POLICY "Allow insert for same school users" ON public.bridge_course_evaluations
  FOR INSERT TO authenticated
  WITH CHECK (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));

DROP POLICY IF EXISTS "Allow update for same school users" ON public.bridge_course_evaluations;
CREATE POLICY "Allow update for same school users" ON public.bridge_course_evaluations
  FOR UPDATE TO authenticated
  USING (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));

DROP POLICY IF EXISTS "Allow delete for same school users" ON public.bridge_course_evaluations;
CREATE POLICY "Allow delete for same school users" ON public.bridge_course_evaluations
  FOR DELETE TO authenticated
  USING (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));


-- 2. Create public.cce_evaluations table
CREATE TABLE IF NOT EXISTS public.cce_evaluations (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  school_id uuid REFERENCES public.schools(id) ON DELETE CASCADE,
  student_id uuid REFERENCES public.admissions(id) ON DELETE CASCADE,
  class_name text NOT NULL,
  exam_type text NOT NULL, -- FA1, FA2, FA3, FA4, SA1, SA2
  marks jsonb NOT NULL DEFAULT '{}'::jsonb, -- {subjectId_mark: float, subjectId_grade: 'A+'/...}
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
  updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
  UNIQUE(student_id, exam_type)
);

-- Enable RLS for cce_evaluations
ALTER TABLE public.cce_evaluations ENABLE ROW LEVEL SECURITY;

-- Policies for cce_evaluations
DROP POLICY IF EXISTS "Allow select cce for same school users" ON public.cce_evaluations;
CREATE POLICY "Allow select cce for same school users" ON public.cce_evaluations
  FOR SELECT TO authenticated
  USING (
    school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid())
    OR (SELECT role FROM public.profiles WHERE id = auth.uid()) = 'developer'
  );

DROP POLICY IF EXISTS "Allow insert cce for same school users" ON public.cce_evaluations;
CREATE POLICY "Allow insert cce for same school users" ON public.cce_evaluations
  FOR INSERT TO authenticated
  WITH CHECK (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));

DROP POLICY IF EXISTS "Allow update cce for same school users" ON public.cce_evaluations;
CREATE POLICY "Allow update cce for same school users" ON public.cce_evaluations
  FOR UPDATE TO authenticated
  USING (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));

DROP POLICY IF EXISTS "Allow delete cce for same school users" ON public.cce_evaluations;
CREATE POLICY "Allow delete cce for same school users" ON public.cce_evaluations
  FOR DELETE TO authenticated
  USING (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));


-- 3. Create public.lba_evaluations table
CREATE TABLE IF NOT EXISTS public.lba_evaluations (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  school_id uuid REFERENCES public.schools(id) ON DELETE CASCADE,
  student_id uuid REFERENCES public.admissions(id) ON DELETE CASCADE,
  class_name text NOT NULL,
  subject_name text NOT NULL,
  lessons jsonb NOT NULL DEFAULT '{}'::jsonb, -- {les_0_mark: float, les_0_grade: 'A+'/...}
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
  updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
  UNIQUE(student_id, subject_name)
);

-- Enable RLS for lba_evaluations
ALTER TABLE public.lba_evaluations ENABLE ROW LEVEL SECURITY;

-- Policies for lba_evaluations
DROP POLICY IF EXISTS "Allow select lba for same school users" ON public.lba_evaluations;
CREATE POLICY "Allow select lba for same school users" ON public.lba_evaluations
  FOR SELECT TO authenticated
  USING (
    school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid())
    OR (SELECT role FROM public.profiles WHERE id = auth.uid()) = 'developer'
  );

DROP POLICY IF EXISTS "Allow insert lba for same school users" ON public.lba_evaluations;
CREATE POLICY "Allow insert lba for same school users" ON public.lba_evaluations
  FOR INSERT TO authenticated
  WITH CHECK (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));

DROP POLICY IF EXISTS "Allow update lba for same school users" ON public.lba_evaluations;
CREATE POLICY "Allow update lba for same school users" ON public.lba_evaluations
  FOR UPDATE TO authenticated
  USING (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));

DROP POLICY IF EXISTS "Allow delete lba for same school users" ON public.lba_evaluations;
CREATE POLICY "Allow delete lba for same school users" ON public.lba_evaluations
  FOR DELETE TO authenticated
  USING (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));
