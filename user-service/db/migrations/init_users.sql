-- Migration for Users table in Supabase
-- Run this script in the Supabase SQL editor

CREATE TYPE user_role AS ENUM ('standard', 'admin');

CREATE TABLE IF NOT EXISTS public.users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role user_role DEFAULT 'standard',
    password_hash VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security (RLS)
ALTER TABLE public.users ENABLE ROW LEVEL SECURITY;

-- Create policy to allow admins to perform all actions
CREATE POLICY "Admins have full access" ON public.users
    FOR ALL
    USING (
        current_setting('request.jwt.claims', true)::json->>'role' = 'admin'
    );

-- Create policy to allow users to read their own data
CREATE POLICY "Users can read own data" ON public.users
    FOR SELECT
    USING (
        id::text = current_setting('request.jwt.claims', true)::json->>'sub'
    );

-- Create policy to allow users to update their own profile
CREATE POLICY "Users can update own profile" ON public.users
    FOR UPDATE
    USING (
        id::text = current_setting('request.jwt.claims', true)::json->>'sub'
    );

-- Create an updated_at trigger function
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Create trigger on users table
DROP TRIGGER IF EXISTS update_users_updated_at ON public.users;
CREATE TRIGGER update_users_updated_at
    BEFORE UPDATE ON public.users
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
