-- SQL Migration Script to create the Attendance Table in Supabase
-- Run this in your Supabase SQL Editor to enable database saving.

CREATE TABLE IF NOT EXISTS public.attendance (
  id uuid DEFAULT gen_random_uuid() PRIMARY KEY,
  school_id uuid REFERENCES public.schools(id) ON DELETE CASCADE,
  student_id uuid REFERENCES public.admissions(id) ON DELETE CASCADE,
  class_name text NOT NULL,
  attendance_type text NOT NULL,
  attendance_date date,
  attendance_month text,
  attendance_year text,
  working_days integer DEFAULT 1,
  present_days integer DEFAULT 0,
  status text,
  remarks text,
  created_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
  updated_at timestamp with time zone DEFAULT timezone('utc'::text, now()) NOT NULL,
  UNIQUE(student_id, attendance_type, attendance_date, attendance_month, attendance_year)
);

-- Enable Row Level Security (RLS)
ALTER TABLE public.attendance ENABLE ROW LEVEL SECURITY;

-- Create Policies for Authenticated Users
CREATE POLICY "Allow select attendance for same school users" ON public.attendance 
  FOR SELECT TO authenticated 
  USING (
    school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()) 
    OR (SELECT role FROM public.profiles WHERE id = auth.uid()) = 'developer'
  );

CREATE POLICY "Allow insert attendance for same school users" ON public.attendance 
  FOR INSERT TO authenticated 
  WITH CHECK (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));

CREATE POLICY "Allow update attendance for same school users" ON public.attendance 
  FOR UPDATE TO authenticated 
  USING (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));

CREATE POLICY "Allow delete attendance for same school users" ON public.attendance 
  FOR DELETE TO authenticated 
  USING (school_id = (SELECT school_id FROM public.profiles WHERE id = auth.uid()));
