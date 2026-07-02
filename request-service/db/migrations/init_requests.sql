-- Migration for Requests table in Supabase
-- Run this script in the Supabase SQL editor or via DB runner

CREATE TABLE IF NOT EXISTS public.requests (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID NOT NULL REFERENCES public.users(id) ON DELETE CASCADE,
    request_type VARCHAR(50) NOT NULL, -- e.g., 'shift_change', 'tool_access'
    title VARCHAR(255) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending', -- 'pending', 'approved', 'rejected'
    auto_approved BOOLEAN DEFAULT false,
    override_by UUID REFERENCES public.users(id) ON DELETE SET NULL,
    override_reason TEXT,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Enable Row Level Security (RLS)
ALTER TABLE public.requests ENABLE ROW LEVEL SECURITY;

-- Create policy to allow admins to perform all actions
CREATE POLICY "Admins have full access on requests" ON public.requests
    FOR ALL
    USING (
        current_setting('request.jwt.claims', true)::json->>'role' = 'admin'
    );

-- Create policy to allow users to read their own requests
CREATE POLICY "Users can read own requests" ON public.requests
    FOR SELECT
    USING (
        user_id::text = current_setting('request.jwt.claims', true)::json->>'sub'
    );

-- Create policy to allow users to insert their own requests
CREATE POLICY "Users can create own requests" ON public.requests
    FOR INSERT
    WITH CHECK (
        user_id::text = current_setting('request.jwt.claims', true)::json->>'sub'
    );

-- Create trigger on requests table for updated_at
DROP TRIGGER IF EXISTS update_requests_updated_at ON public.requests;
CREATE TRIGGER update_requests_updated_at
    BEFORE UPDATE ON public.requests
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
