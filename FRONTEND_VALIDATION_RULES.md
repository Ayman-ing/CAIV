# Frontend Validation Rules to Implement

## Summary of Backend Validations to Apply to Frontend

### Profile Links
- `label`: min_length=1, max_length=200
- `url`: HttpUrl (valid HTTP/HTTPS URL)
- `platform`: Required, enum

### Skills
- `category`: min_length=1, max_length=100
- `name`: min_length=1, max_length=200
- `proficiency`: Optional, enum
- `years_experience`: ge=0, le=50

### Work Experience
- `job_title`: min_length=1, max_length=200
- `company`: min_length=1, max_length=200
- `start_date`: Required, date
- `end_date`: date, must be after start_date (if provided)
- `description`: max_length=2000

### Languages
- `language`: min_length=1, max_length=100
- `proficiency`: Required, enum
- `can_read`: Optional boolean
- `can_write`: Optional boolean
- `can_speak`: Optional boolean

### Education
- `institution`: min_length=1, max_length=200
- `degree`: min_length=1, max_length=200
- `field_of_study`: max_length=200
- `honors`: max_length=200
- `gpa`: ge=0.0, le=20.0
- `start_date`: Required, date
- `end_date`: date, must be after start_date (if provided)
- `description`: max_length=1000

### Projects
- `name`: min_length=1, max_length=200
- `description`: max_length=2000
- `start_date`: Required, date
- `end_date`: date, must be after start_date (if provided)
- `url`: Optional HttpUrl (valid HTTP/HTTPS URL)
- `technologies`: max_length=1000

### Custom Sections
- `title`: min_length=1, max_length=255
- `content`: min_length=1, max_length=10000 (with trimming validation)
- `order_index`: ge=0, le=100

### Certificates
- Check schema for validation rules needed

## Implementation Status

- ✅ useUrlValidator.ts - Created
- ✅ useFormValidation.ts - Created  
- ✅ LinksSection - Partial (label + URL validation done)
- 🔄 ProjectSection - In progress (need to finish template updates)
- ⏳ EducationSection - Needs updates
- ⏳ ExperienceSection - Needs updates
- ⏳ SkillsSection - Needs updates
- ⏳ LanguageSection - Needs updates
- ⏳ CustomSection - Needs updates
- ⏳ CertificationSection - Needs review

## Key validation features to add:
1. Character count indicators (show current/max characters)
2. Real-time validation errors
3. Disabled submit button if validation fails
4. Min/Max value indicators
5. Date comparison validation (end > start)
6. Length validation with user-friendly messages
7. Required field indicators
