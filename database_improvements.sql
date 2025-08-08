"""Schema improvements for AI Resume Builder

This script contains the recommended improvements for the database schema.
Run these incrementally and test thoroughly in development first.
"""

-- ============================================================================
-- PHASE 1: CRITICAL PERFORMANCE INDEXES
-- ============================================================================

-- Foreign key indexes for better join performance
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_profiles_user_id ON profiles(user_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_generated_resumes_profile_id ON generated_resumes(profile_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_generated_resumes_job_description_id ON generated_resumes(job_description_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_resume_components_generated_resume_id ON resume_components(generated_resume_id);

-- Profile detail table indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_education_profile_id ON education(profile_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_work_experiences_profile_id ON work_experiences(profile_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_projects_profile_id ON projects(profile_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_skills_profile_id ON skills(profile_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_certificates_profile_id ON certificates(profile_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_languages_profile_id ON languages(profile_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_professional_summaries_profile_id ON professional_summaries(profile_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_profile_links_profile_id ON profile_links(profile_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_custom_sections_profile_id ON custom_sections(profile_id);

-- Job-related indexes
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_job_keywords_job_description_id ON job_keywords(job_description_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_job_requirements_job_description_id ON job_requirements(job_description_id);

-- UUID lookups (API access)
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_uuid ON users(uuid);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_profiles_uuid ON profiles(uuid);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_generated_resumes_uuid ON generated_resumes(uuid);

-- Authentication
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_users_email ON users(email);

-- ============================================================================
-- PHASE 2: DATA VALIDATION CONSTRAINTS
-- ============================================================================

-- Email format validation
DO $$
BEGIN
    ALTER TABLE users ADD CONSTRAINT chk_users_email_format 
      CHECK (email ~* '^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$');
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

-- Proficiency level constraints
DO $$
BEGIN
    ALTER TABLE skills ADD CONSTRAINT chk_skills_proficiency 
      CHECK (proficiency IN ('Beginner', 'Intermediate', 'Advanced', 'Expert'));
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE languages ADD CONSTRAINT chk_languages_proficiency 
      CHECK (proficiency IN ('Basic', 'Conversational', 'Professional', 'Native'));
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

-- Date validation constraints
DO $$
BEGIN
    ALTER TABLE education ADD CONSTRAINT chk_education_dates 
      CHECK (end_date IS NULL OR end_date >= start_date);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE work_experiences ADD CONSTRAINT chk_work_experience_dates 
      CHECK (end_date IS NULL OR end_date >= start_date);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE projects ADD CONSTRAINT chk_project_dates 
      CHECK (end_date IS NULL OR end_date >= start_date);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

DO $$
BEGIN
    ALTER TABLE certificates ADD CONSTRAINT chk_certificate_dates 
      CHECK (expiration_date IS NULL OR expiration_date >= issue_date);
EXCEPTION
    WHEN duplicate_object THEN NULL;
END $$;

-- ============================================================================
-- PHASE 3: AUDIT TRAIL SYSTEM
-- ============================================================================

CREATE TABLE IF NOT EXISTS audit_log (
    id SERIAL PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    record_id INTEGER NOT NULL,
    action VARCHAR(10) NOT NULL, -- INSERT, UPDATE, DELETE
    old_values JSONB,
    new_values JSONB,
    changed_by INTEGER REFERENCES users(id),
    changed_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_audit_log_table_record ON audit_log(table_name, record_id);
CREATE INDEX IF NOT EXISTS idx_audit_log_changed_at ON audit_log(changed_at);

-- ============================================================================
-- PHASE 4: ENHANCED VECTOR EMBEDDINGS
-- ============================================================================

-- Add columns for better vector embedding management
DO $$
BEGIN
    ALTER TABLE vector_embeddings ADD COLUMN IF NOT EXISTS embedding_model VARCHAR(100);
    ALTER TABLE vector_embeddings ADD COLUMN IF NOT EXISTS embedding_version VARCHAR(20);
    ALTER TABLE vector_embeddings ADD COLUMN IF NOT EXISTS content_hash VARCHAR(64);
    ALTER TABLE vector_embeddings ADD COLUMN IF NOT EXISTS embedding_dimensions INTEGER;
END $$;

-- Indexes for vector embeddings
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_vector_embeddings_entity ON vector_embeddings(entity_type, entity_id);
CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_vector_embeddings_model ON vector_embeddings(embedding_model);

-- ============================================================================
-- PHASE 5: RESUME TEMPLATES SYSTEM
-- ============================================================================

CREATE TABLE IF NOT EXISTS resume_templates (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    name VARCHAR(100) NOT NULL,
    description TEXT,
    industry VARCHAR(50),
    template_data JSONB NOT NULL,
    is_active BOOLEAN DEFAULT true,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

-- Add template reference to generated resumes
DO $$
BEGIN
    ALTER TABLE generated_resumes ADD COLUMN IF NOT EXISTS template_id INTEGER REFERENCES resume_templates(id);
END $$;

-- ============================================================================
-- PHASE 6: RESUME SHARING AND COLLABORATION
-- ============================================================================

CREATE TABLE IF NOT EXISTS resume_shares (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    resume_id INTEGER NOT NULL REFERENCES generated_resumes(id),
    shared_by INTEGER NOT NULL REFERENCES users(id),
    shared_with_email VARCHAR(255),
    access_level VARCHAR(20) DEFAULT 'view',
    expires_at TIMESTAMP,
    access_count INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS resume_feedback (
    id SERIAL PRIMARY KEY,
    uuid UUID UNIQUE NOT NULL DEFAULT gen_random_uuid(),
    resume_id INTEGER NOT NULL REFERENCES generated_resumes(id),
    section_id VARCHAR(50),
    feedback_text TEXT NOT NULL,
    feedback_type VARCHAR(20) DEFAULT 'suggestion',
    given_by_email VARCHAR(255),
    created_at TIMESTAMP DEFAULT NOW()
);

-- ============================================================================
-- PHASE 7: ANALYTICS AND REPORTING
-- ============================================================================

CREATE TABLE IF NOT EXISTS user_activity (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id),
    activity_type VARCHAR(50) NOT NULL,
    entity_type VARCHAR(50),
    entity_id INTEGER,
    metadata JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_user_activity_user_id ON user_activity(user_id);
CREATE INDEX IF NOT EXISTS idx_user_activity_type ON user_activity(activity_type);
CREATE INDEX IF NOT EXISTS idx_user_activity_created_at ON user_activity(created_at);

CREATE TABLE IF NOT EXISTS resume_stats (
    id SERIAL PRIMARY KEY,
    resume_id INTEGER NOT NULL REFERENCES generated_resumes(id),
    views_count INTEGER DEFAULT 0,
    downloads_count INTEGER DEFAULT 0,
    last_viewed_at TIMESTAMP,
    last_downloaded_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE UNIQUE INDEX IF NOT EXISTS idx_resume_stats_resume_id ON resume_stats(resume_id);

-- ============================================================================
-- PHASE 8: SOFT DELETE FUNCTIONALITY
-- ============================================================================

-- Add soft delete columns
DO $$
BEGIN
    ALTER TABLE users ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP;
    ALTER TABLE profiles ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP;
    ALTER TABLE generated_resumes ADD COLUMN IF NOT EXISTS deleted_at TIMESTAMP;
END $$;

-- Create views for active records
CREATE OR REPLACE VIEW active_users AS 
    SELECT * FROM users WHERE deleted_at IS NULL;

CREATE OR REPLACE VIEW active_profiles AS 
    SELECT * FROM profiles WHERE deleted_at IS NULL;

CREATE OR REPLACE VIEW active_resumes AS 
    SELECT * FROM generated_resumes WHERE deleted_at IS NULL;

-- ============================================================================
-- PHASE 9: COMPUTED COLUMNS FOR ANALYTICS
-- ============================================================================

-- Add computed fields
DO $$
BEGIN
    ALTER TABLE profiles ADD COLUMN IF NOT EXISTS total_experience_months INTEGER;
    ALTER TABLE profiles ADD COLUMN IF NOT EXISTS skill_count INTEGER;
    ALTER TABLE profiles ADD COLUMN IF NOT EXISTS education_level VARCHAR(50);
END $$;

-- Function to update profile statistics
CREATE OR REPLACE FUNCTION update_profile_stats()
RETURNS TRIGGER AS $$
BEGIN
    -- Calculate total experience in months
    UPDATE profiles SET 
        total_experience_months = (
            SELECT COALESCE(SUM(
                EXTRACT(YEAR FROM AGE(COALESCE(end_date, CURRENT_DATE), start_date)) * 12 +
                EXTRACT(MONTH FROM AGE(COALESCE(end_date, CURRENT_DATE), start_date))
            ), 0)
            FROM work_experiences 
            WHERE profile_id = COALESCE(NEW.profile_id, OLD.profile_id)
        ),
        skill_count = (
            SELECT COUNT(*) 
            FROM skills 
            WHERE profile_id = COALESCE(NEW.profile_id, OLD.profile_id)
        )
    WHERE id = COALESCE(NEW.profile_id, OLD.profile_id);
    
    RETURN COALESCE(NEW, OLD);
END;
$$ LANGUAGE plpgsql;

-- Triggers to maintain profile stats
DROP TRIGGER IF EXISTS trg_update_profile_stats_work ON work_experiences;
CREATE TRIGGER trg_update_profile_stats_work
    AFTER INSERT OR UPDATE OR DELETE ON work_experiences
    FOR EACH ROW EXECUTE FUNCTION update_profile_stats();

DROP TRIGGER IF EXISTS trg_update_profile_stats_skills ON skills;
CREATE TRIGGER trg_update_profile_stats_skills
    AFTER INSERT OR UPDATE OR DELETE ON skills
    FOR EACH ROW EXECUTE FUNCTION update_profile_stats();

-- ============================================================================
-- PHASE 10: FULL-TEXT SEARCH PREPARATION
-- ============================================================================

-- Add search vector columns
DO $$
BEGIN
    ALTER TABLE job_descriptions ADD COLUMN IF NOT EXISTS search_vector tsvector;
    ALTER TABLE generated_resumes ADD COLUMN IF NOT EXISTS search_vector tsvector;
    ALTER TABLE work_experiences ADD COLUMN IF NOT EXISTS search_vector tsvector;
    ALTER TABLE projects ADD COLUMN IF NOT EXISTS search_vector tsvector;
END $$;

-- Function to update search vectors
CREATE OR REPLACE FUNCTION update_search_vector()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_TABLE_NAME = 'job_descriptions' THEN
        NEW.search_vector := to_tsvector('english', 
            COALESCE(NEW.title, '') || ' ' || 
            COALESCE(NEW.company, '') || ' ' || 
            COALESCE(NEW.description, '')
        );
    ELSIF TG_TABLE_NAME = 'generated_resumes' THEN
        NEW.search_vector := to_tsvector('english', 
            COALESCE(NEW.title, '') || ' ' || 
            COALESCE(NEW.content, '')
        );
    ELSIF TG_TABLE_NAME = 'work_experiences' THEN
        NEW.search_vector := to_tsvector('english', 
            COALESCE(NEW.company, '') || ' ' || 
            COALESCE(NEW.position, '') || ' ' || 
            COALESCE(NEW.description, '')
        );
    ELSIF TG_TABLE_NAME = 'projects' THEN
        NEW.search_vector := to_tsvector('english', 
            COALESCE(NEW.name, '') || ' ' || 
            COALESCE(NEW.description, '') || ' ' || 
            COALESCE(NEW.technologies, '')
        );
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Triggers for search vector updates
DROP TRIGGER IF EXISTS trg_job_descriptions_search ON job_descriptions;
CREATE TRIGGER trg_job_descriptions_search
    BEFORE INSERT OR UPDATE ON job_descriptions
    FOR EACH ROW EXECUTE FUNCTION update_search_vector();

DROP TRIGGER IF EXISTS trg_generated_resumes_search ON generated_resumes;
CREATE TRIGGER trg_generated_resumes_search
    BEFORE INSERT OR UPDATE ON generated_resumes
    FOR EACH ROW EXECUTE FUNCTION update_search_vector();

DROP TRIGGER IF EXISTS trg_work_experiences_search ON work_experiences;
CREATE TRIGGER trg_work_experiences_search
    BEFORE INSERT OR UPDATE ON work_experiences
    FOR EACH ROW EXECUTE FUNCTION update_search_vector();

DROP TRIGGER IF EXISTS trg_projects_search ON projects;
CREATE TRIGGER trg_projects_search
    BEFORE INSERT OR UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_search_vector();

-- Create GIN indexes for full-text search (run these during low-traffic periods)
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_job_descriptions_search ON job_descriptions USING GIN(search_vector);
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_generated_resumes_search ON generated_resumes USING GIN(search_vector);
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_work_experiences_search ON work_experiences USING GIN(search_vector);
-- CREATE INDEX CONCURRENTLY IF NOT EXISTS idx_projects_search ON projects USING GIN(search_vector);

-- ============================================================================
-- INITIAL DATA FOR RESUME TEMPLATES
-- ============================================================================

INSERT INTO resume_templates (name, description, industry, template_data) VALUES
('Modern Tech Resume', 'Clean, modern template for software engineers and tech professionals', 'Technology', 
 '{"sections": ["summary", "experience", "skills", "projects", "education"], "style": "modern", "colors": {"primary": "#2563eb", "secondary": "#64748b"}}'),
('Executive Professional', 'Formal template for senior management and executive positions', 'Business', 
 '{"sections": ["summary", "experience", "achievements", "education", "skills"], "style": "executive", "colors": {"primary": "#1f2937", "secondary": "#6b7280"}}'),
('Creative Portfolio', 'Artistic template for designers and creative professionals', 'Creative', 
 '{"sections": ["summary", "experience", "projects", "skills", "education"], "style": "creative", "colors": {"primary": "#7c3aed", "secondary": "#a78bfa"}}'),
('Academic Research', 'Template for researchers and academic professionals', 'Academic', 
 '{"sections": ["summary", "education", "experience", "publications", "skills"], "style": "academic", "colors": {"primary": "#059669", "secondary": "#10b981"}}')
ON CONFLICT (name) DO NOTHING;

COMMIT;
