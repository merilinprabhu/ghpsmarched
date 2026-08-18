-- ==============================================================================
-- SAFE FIX FOR SUPABASE: ADD MISSING COLUMNS TO ADMISSIONS & CREATE TC TABLES
-- Fixes ERROR 42703 (column "status" does not exist)
-- ==============================================================================

-- Step 1: Ensure admissions table exists
CREATE TABLE IF NOT EXISTS public.admissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Step 2: Safely add status and all required TC columns if they don't exist yet
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS school_id TEXT DEFAULT '2909709801';
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS app_no TEXT;
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS student_sts TEXT;
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS sts_no TEXT;
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS student_name TEXT;
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS name_english TEXT;
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS name_kannada TEXT;
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS father_name TEXT;
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS mother_name TEXT;
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS dob DATE;
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS gender TEXT;
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS nationality TEXT DEFAULT 'Indian/ಭಾರತೀಯ';
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS religion TEXT DEFAULT 'Hindu / ಹಿಂದು';
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS caste TEXT;
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS social_class TEXT DEFAULT 'SC / ಎಸ್ಸಿ';
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS enroll_class TEXT DEFAULT 'Class 7';
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS medium TEXT DEFAULT 'Kannada / ಕನ್ನಡ';
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS district TEXT DEFAULT 'RAICHUR';
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS taluk TEXT DEFAULT 'Raichur';
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS village TEXT DEFAULT 'Merched';
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS address TEXT;
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS date_of_admission DATE;
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS fees_paid TEXT DEFAULT 'YES / ಹೌದು';
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS fee_concession TEXT DEFAULT 'NIL';
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS scholarship TEXT DEFAULT 'NIL';
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS medically_examined TEXT DEFAULT 'YES / ಹೌದು';
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS status TEXT DEFAULT 'ACTIVE';
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS transfer_no TEXT;
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS transfer_date DATE;
ALTER TABLE public.admissions ADD COLUMN IF NOT EXISTS updated_at TIMESTAMPTZ DEFAULT NOW();

-- Enable RLS and Create Policy for Admissions
ALTER TABLE public.admissions ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow public read/write access to admissions" ON public.admissions;
CREATE POLICY "Allow public read/write access to admissions" ON public.admissions FOR ALL USING (true) WITH CHECK (true);

-- Step 3: Create TC Register table for historical logs
CREATE TABLE IF NOT EXISTS public.tc_register (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    school_id TEXT DEFAULT '2909709801',
    student_id UUID REFERENCES public.admissions(id) ON DELETE SET NULL,
    tc_no TEXT NOT NULL,
    sts_no TEXT NOT NULL,
    student_name TEXT NOT NULL,
    enroll_class TEXT,
    academic_year TEXT DEFAULT '2026-2027',
    date_of_entry DATE DEFAULT CURRENT_DATE,
    date_of_issue DATE DEFAULT CURRENT_DATE,
    reason_for_leaving TEXT,
    conduct TEXT DEFAULT 'Good / ಉತ್ತಮವಾಗಿದೆ',
    tc_type TEXT DEFAULT 'TC',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Enable RLS and Create Policy for TC Register
ALTER TABLE public.tc_register ENABLE ROW LEVEL SECURITY;
DROP POLICY IF EXISTS "Allow public read/write access to tc_register" ON public.tc_register;
CREATE POLICY "Allow public read/write access to tc_register" ON public.tc_register FOR ALL USING (true) WITH CHECK (true);

-- Step 4: Create Indexes Safely
CREATE INDEX IF NOT EXISTS idx_admissions_status ON public.admissions(status);
CREATE INDEX IF NOT EXISTS idx_admissions_app_no ON public.admissions(app_no);
CREATE INDEX IF NOT EXISTS idx_tc_register_sts_no ON public.tc_register(sts_no);
CREATE INDEX IF NOT EXISTS idx_tc_register_tc_no ON public.tc_register(tc_no);
