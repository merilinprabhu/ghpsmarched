-- SQL script to add missing columns to public.profiles table
-- Execute this script in your Supabase SQL Editor (https://supabase.com/dashboard)

-- 1. Add is_approved column if it does not exist
ALTER TABLE public.profiles
ADD COLUMN IF NOT EXISTS is_approved boolean DEFAULT false;

-- 2. Add assigned_classes column if it does not exist
ALTER TABLE public.profiles
ADD COLUMN IF NOT EXISTS assigned_classes jsonb DEFAULT '[]'::jsonb;
