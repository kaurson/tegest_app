-- Simple Test Schema for Estonian Learning App
-- This is a minimal version for testing only

-- Enable UUID extension
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Simple lessons table (adapted from existing structure)
CREATE TABLE IF NOT EXISTS lessons (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    session_id UUID UNIQUE NOT NULL,
    user_id TEXT DEFAULT 'test_user',
    title TEXT NOT NULL,
    description TEXT,
    steps TEXT[] NOT NULL,
    step_statuses TEXT[] NOT NULL DEFAULT ARRAY[]::TEXT[],
    step_responses JSONB[] NOT NULL DEFAULT ARRAY[]::JSONB[],
    current_step_index INTEGER DEFAULT 0,
    status TEXT DEFAULT 'not_started',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Simple index for performance
CREATE INDEX IF NOT EXISTS idx_lessons_session_id ON lessons(session_id);

-- Function to update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Trigger for updated_at
CREATE TRIGGER update_lessons_updated_at 
    BEFORE UPDATE ON lessons 
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column(); 