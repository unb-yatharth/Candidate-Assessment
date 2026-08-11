-- SQL Schema for Candidate Assessment System in Supabase (Idempotent & Safe to Re-run)

-- 1. Create candidate_assessments table
CREATE TABLE IF NOT EXISTS candidate_assessments (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    candidate_name TEXT NOT NULL,
    candidate_email TEXT NOT NULL,
    candidate_phone TEXT,
    invigilator_name TEXT,
    role_applied TEXT,
    assessment_level TEXT,
    access_password TEXT, -- Optional / nullable so candidate insert succeeds
    submission_payload JSONB NOT NULL,
    status TEXT DEFAULT 'submitted',
    mcq_score NUMERIC,
    written_score NUMERIC,
    total_score NUMERIC,
    created_at TIMESTAMPTZ DEFAULT NOW(),
    graded_at TIMESTAMPTZ
);

-- Ensure access_password column is NULLABLE if table was created previously with NOT NULL
ALTER TABLE candidate_assessments ALTER COLUMN access_password DROP NOT NULL;

-- 2. Create indexes for fast search and filtering in HR Dashboard
CREATE INDEX IF NOT EXISTS idx_candidate_email ON candidate_assessments(candidate_email);
CREATE INDEX IF NOT EXISTS idx_created_at ON candidate_assessments(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_status ON candidate_assessments(status);

-- 3. Enable Row Level Security (RLS)
ALTER TABLE candidate_assessments ENABLE ROW LEVEL SECURITY;

-- 4. Re-create RLS Policies safely by dropping existing ones first
DROP POLICY IF EXISTS "Allow public assessment submission" ON candidate_assessments;
DROP POLICY IF EXISTS "Allow public select for HR Dashboard" ON candidate_assessments;
DROP POLICY IF EXISTS "Allow update for assessment scoring" ON candidate_assessments;
DROP POLICY IF EXISTS "Allow candidates to view their own results" ON candidate_assessments;

-- Allow anyone to submit an assessment (insert)
CREATE POLICY "Allow public assessment submission" 
ON candidate_assessments FOR INSERT 
WITH CHECK (true);

-- Allow selecting records for HR Dashboard
CREATE POLICY "Allow public select for HR Dashboard" 
ON candidate_assessments FOR SELECT 
USING (true);

-- Allow updating records for HR grading
CREATE POLICY "Allow update for assessment scoring" 
ON candidate_assessments FOR UPDATE 
USING (true);