-- Attendance Table Schema for GHPS Marched School Management System
CREATE TABLE IF NOT EXISTS public.attendance (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id TEXT,
    student_id UUID NOT NULL REFERENCES public.admissions(id) ON DELETE CASCADE,
    class_name TEXT NOT NULL,
    attendance_type TEXT NOT NULL, -- 'daily', 'monthly', 'yearly'
    attendance_date DATE,          -- for daily
    attendance_month TEXT,         -- e.g. '2026-06' for monthly
    attendance_year TEXT,          -- e.g. '2026-27' for yearly
    working_days INT DEFAULT 1,
    present_days INT DEFAULT 0,
    status TEXT,                   -- 'present', 'absent'
    remarks TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),
    CONSTRAINT unique_student_attendance UNIQUE (student_id, attendance_type, attendance_date, attendance_month, attendance_year)
);

-- Enable RLS & Create Policies
ALTER TABLE public.attendance ENABLE ROW LEVEL SECURITY;
CREATE POLICY "Allow public read/write access to attendance" ON public.attendance FOR ALL USING (true) WITH CHECK (true);
