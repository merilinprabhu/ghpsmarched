-- 1. Ensure assigned_classes column exists in teachers table
ALTER TABLE public.teachers
ADD COLUMN IF NOT EXISTS assigned_classes jsonb DEFAULT '[]'::jsonb;

-- 2. Drop existing update policy if any on profiles table
DROP POLICY IF EXISTS "Allow admins to update all profiles" ON public.profiles;

-- 3. Create RLS policy for profiles table updates
-- This policy allows Admins and developers to update any profile, preventing infinite recursion by using JWT metadata
CREATE POLICY "Allow admins to update all profiles" 
ON public.profiles 
FOR UPDATE 
TO authenticated 
USING (
  coalesce(auth.jwt() -> 'user_metadata' ->> 'role', '') IN ('Admin', 'developer')
)
WITH CHECK (
  coalesce(auth.jwt() -> 'user_metadata' ->> 'role', '') IN ('Admin', 'developer')
);

-- 4. Ensure SELECT policy also allows admins to read all profiles
DROP POLICY IF EXISTS "Allow admins to select all profiles" ON public.profiles;
CREATE POLICY "Allow admins to select all profiles" 
ON public.profiles 
FOR SELECT 
TO authenticated 
USING (
  coalesce(auth.jwt() -> 'user_metadata' ->> 'role', '') IN ('Admin', 'developer')
  OR school_id = (coalesce(auth.jwt() -> 'user_metadata' ->> 'school_id', '00000000-0000-0000-0000-000000000000'))::uuid
);
