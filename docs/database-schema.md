# Database Schema Documentation

## Overview

The AI Resume Builder uses a PostgreSQL database with a profile-based architecture that separates user authentication from resume-related data. This design allows users to maintain multiple professional profiles for different career paths or industries.

## Database Tables

### Core Tables

#### `users`
Primary authentication and contact information for users.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| email | String | User email address (unique) |
| location | String | User location |
| phone_number | String | User phone number |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

**Relationships:**
- One-to-many with `profiles`
- One-to-many with `job_descriptions`

#### `profiles`
Professional profiles associated with users. Users can have multiple profiles.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| user_id | Integer | Foreign key to users.id |
| name | String | Profile name/title |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

**Relationships:**
- Many-to-one with `users`
- One-to-many with all profile detail tables
- One-to-many with `generated_resumes`

#### `generated_resumes`
Complete generated resume documents.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| profile_id | Integer | Foreign key to profiles.id |
| job_description_id | Integer | Foreign key to job_descriptions.id |
| title | String | Resume title |
| content | Text | Complete resume content |
| format | String | Resume format (pdf, docx, etc.) |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

**Relationships:**
- Many-to-one with `profiles`
- Many-to-one with `job_descriptions`
- One-to-many with `resume_components`

#### `resume_components`
Individual sections/components of resumes.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| generated_resume_id | Integer | Foreign key to generated_resumes.id |
| component_type | String | Type of component (summary, experience, etc.) |
| content | Text | Component content |
| order_index | Integer | Display order |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

### Job-Related Tables

#### `job_descriptions`
Job postings and requirements for resume generation.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| user_id | Integer | Foreign key to users.id |
| title | String | Job title |
| company | String | Company name |
| description | Text | Full job description |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

**Relationships:**
- Many-to-one with `users`
- One-to-many with `job_keywords`
- One-to-many with `job_requirements`
- One-to-many with `generated_resumes`

#### `job_keywords`
Extracted keywords from job descriptions.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| job_description_id | Integer | Foreign key to job_descriptions.id |
| keyword | String | Extracted keyword |
| importance_score | Float | Relevance score |

#### `job_requirements`
Structured requirements extracted from job descriptions.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| job_description_id | Integer | Foreign key to job_descriptions.id |
| requirement_type | String | Type of requirement |
| description | String | Requirement description |
| is_required | Boolean | Whether requirement is mandatory |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

### Profile Detail Tables

All profile detail tables follow a similar pattern with profile_id foreign key.

#### `education`
Educational background information.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| profile_id | Integer | Foreign key to profiles.id |
| institution | String | Educational institution name |
| degree | String | Degree type |
| field_of_study | String | Major/field of study |
| start_date | Date | Start date |
| end_date | Date | End date (null if current) |
| gpa | String | Grade point average |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

#### `work_experiences`
Professional work history.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| profile_id | Integer | Foreign key to profiles.id |
| company | String | Company name |
| position | String | Job position/title |
| description | Text | Job description |
| start_date | Date | Start date |
| end_date | Date | End date (null if current) |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

#### `projects`
Personal and professional projects.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| profile_id | Integer | Foreign key to profiles.id |
| name | String | Project name |
| description | Text | Project description |
| technologies | String | Technologies used |
| start_date | Date | Start date |
| end_date | Date | End date |
| url | String | Project URL |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

#### `skills`
Technical and soft skills.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| profile_id | Integer | Foreign key to profiles.id |
| name | String | Skill name |
| category | String | Skill category |
| proficiency | String | Proficiency level |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

#### `certificates`
Professional certifications and licenses.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| profile_id | Integer | Foreign key to profiles.id |
| name | String | Certificate name |
| issuing_organization | String | Issuing organization |
| issue_date | Date | Issue date |
| expiration_date | Date | Expiration date |
| credential_id | String | Credential ID |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

#### `languages`
Language proficiencies.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| profile_id | Integer | Foreign key to profiles.id |
| language | String | Language name |
| proficiency | String | Proficiency level |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

#### `professional_summaries`
Professional summary variants.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| profile_id | Integer | Foreign key to profiles.id |
| title | String | Summary title |
| content | Text | Summary content |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

#### `profile_links`
Social media and professional links.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| profile_id | Integer | Foreign key to profiles.id |
| platform | String | Platform name |
| url | String | Profile URL |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

#### `custom_sections`
Custom resume sections.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| profile_id | Integer | Foreign key to profiles.id |
| title | String | Section title |
| content | Text | Section content |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

### System Tables

#### `outbox_events`
Event sourcing for reliable system events.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| event_type | String | Type of event |
| entity_type | String | Entity type affected |
| entity_id | Integer | Entity ID affected |
| payload | JSON | Event payload data |
| processed | Boolean | Whether event was processed |
| error | String | Error message if processing failed |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

#### `vector_embeddings`
AI embeddings for intelligent matching.

| Column | Type | Description |
|--------|------|-------------|
| id | Integer | Primary key |
| uuid | UUID | Public UUID for API access |
| entity_type | String | Type of entity (profile, job_description) |
| entity_id | Integer | ID of related entity |
| qdrant_point_id | UUID | ID in Qdrant vector database |
| chunk_index | Integer | Chunk index for large content |
| metadata_json | Text | JSON metadata about embedding |
| created_at | DateTime | Record creation timestamp |
| updated_at | DateTime | Record update timestamp |

## Database Relationships

### Primary Relationships

```
Users (1) ←→ (M) Profiles
Users (1) ←→ (M) JobDescriptions
Profiles (1) ←→ (M) GeneratedResumes
JobDescriptions (1) ←→ (M) GeneratedResumes
GeneratedResumes (1) ←→ (M) ResumeComponents
```

### Profile Detail Relationships

All profile detail tables have a many-to-one relationship with Profiles:

```
Profiles (1) ←→ (M) Education
Profiles (1) ←→ (M) WorkExperiences
Profiles (1) ←→ (M) Projects
Profiles (1) ←→ (M) Skills
Profiles (1) ←→ (M) Certificates
Profiles (1) ←→ (M) Languages
Profiles (1) ←→ (M) ProfessionalSummaries
Profiles (1) ←→ (M) ProfileLinks
Profiles (1) ←→ (M) CustomSections
```

### Job Analysis Relationships

```
JobDescriptions (1) ←→ (M) JobKeywords
JobDescriptions (1) ←→ (M) JobRequirements
```

## Migration History

- **Initial Migration**: `a86c4bf958f7_create_all_tables_complete_schema.py`
  - Created all 18 tables with proper relationships
  - Established foreign key constraints
  - Set up UUID and timestamp columns

## Indexes and Performance

### Recommended Indexes

```sql
-- User lookups
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_uuid ON users(uuid);

-- Profile lookups
CREATE INDEX idx_profiles_user_id ON profiles(user_id);
CREATE INDEX idx_profiles_uuid ON profiles(uuid);

-- Resume generation
CREATE INDEX idx_generated_resumes_profile_id ON generated_resumes(profile_id);
CREATE INDEX idx_generated_resumes_job_description_id ON generated_resumes(job_description_id);

-- Profile details
CREATE INDEX idx_education_profile_id ON education(profile_id);
CREATE INDEX idx_work_experiences_profile_id ON work_experiences(profile_id);
-- ... (similar indexes for other profile detail tables)

-- Job analysis
CREATE INDEX idx_job_keywords_job_description_id ON job_keywords(job_description_id);
CREATE INDEX idx_job_requirements_job_description_id ON job_requirements(job_description_id);

-- Vector embeddings
CREATE INDEX idx_vector_embeddings_entity ON vector_embeddings(entity_type, entity_id);
```

## Data Integrity

### Foreign Key Constraints

All foreign key relationships are enforced at the database level to ensure referential integrity.

### UUID Usage

- All tables include a `uuid` field for external API access
- UUIDs provide security by obscuring internal database IDs
- Internal `id` fields remain for performance optimization

### Timestamps

- All tables include `created_at` and `updated_at` timestamps
- Timestamps use UTC timezone
- Automatic updates handled by SQLAlchemy
