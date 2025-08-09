# Schema Validation Enhancements

## Overview

This document outlines the comprehensive enhancements made to all Pydantic schemas in the AIResumeBuilder application. These improvements add robust validation, better error handling, and align with the new hierarchical API structure.

## Updated Schema Files

### 1. Work Experiences Schema (`app/features/profiles/work_experiences/schemas.py`)

**Enhancements:**
- Added Field validation with constraints (min_length, max_length, ge, le)
- Custom validators for date validation and business logic
- Enhanced documentation with proper field descriptions
- Added profile_id relationship field
- Removed user_uuid references

**Key Validations:**
- Company name: 1-255 characters, non-empty
- Job title: 1-255 characters, non-empty
- Date validation: start_date cannot be in future, end_date cannot be before start_date
- Salary validation: non-negative values
- Description: max 5000 characters

### 2. Skills Schema (`app/features/profiles/skills/schemas.py`)

**Enhancements:**
- Skill name validation with character limits
- Proficiency level enum with validation
- Years of experience validation (0-50 years)
- Category validation with predefined options
- Enhanced error messages

**Key Validations:**
- Skill name: 1-100 characters, non-empty
- Proficiency: BEGINNER, INTERMEDIATE, ADVANCED, EXPERT
- Years of experience: 0-50 range
- Category: technical, soft, language, tool, certification

### 3. Projects Schema (`app/features/profiles/projects/schemas.py`)

**Enhancements:**
- Project name and description validation
- URL validation for project links
- Technology stack validation
- Date range validation
- Status tracking with enums

**Key Validations:**
- Project name: 1-255 characters
- Description: max 5000 characters
- Technologies: list of strings with validation
- Date validation: logical date ranges
- URL validation: proper HTTP/HTTPS format

### 4. Education Schema (`app/features/profiles/education/schemas.py`)

**Enhancements:**
- Institution and degree validation
- GPA validation with proper ranges
- Date validation for academic periods
- Field of study validation
- Achievement tracking

**Key Validations:**
- Institution: 1-255 characters, non-empty
- Degree: 1-255 characters, non-empty
- GPA: 0.0-4.0 range (US standard)
- Date validation: graduation date logic
- Field of study: max 255 characters

### 5. Certificates Schema (`app/features/profiles/certificates/schemas.py`)

**Enhancements:**
- Certificate name and issuer validation
- Expiration date handling
- Credential ID validation
- URL validation for certificate links
- Status tracking (active, expired, pending)

**Key Validations:**
- Certificate name: 1-255 characters
- Issuing organization: 1-255 characters
- Credential ID: alphanumeric validation
- Expiration logic: cannot be in the past for active certificates
- URL validation: proper format for verification links

### 6. Languages Schema (`app/features/profiles/languages/schemas.py`)

**Enhancements:**
- Language name validation
- Proficiency level standardization
- Certification tracking
- Native language identification
- Multiple proficiency frameworks support

**Key Validations:**
- Language name: 1-100 characters
- Proficiency: standardized levels (A1, A2, B1, B2, C1, C2, Native)
- Certification validation
- Boolean flags for native/business proficiency

### 7. Custom Sections Schema (`app/features/profiles/custom_sections/schemas.py`)

**Enhancements:**
- Title and content validation
- Order index management
- Rich text content support
- Template-based sections
- Display order optimization

**Key Validations:**
- Title: 1-255 characters, non-empty
- Content: 1-10000 characters, non-empty
- Order index: 0-100 range
- Whitespace trimming and validation

### 8. Profile Links Schema (`app/features/profiles/profile_links/schemas.py`)

**Enhancements:**
- Platform-specific URL validation
- Social media platform enumeration
- Domain validation for known platforms
- Professional link categorization
- URL format validation

**Key Validations:**
- Platform: predefined enum values
- URL: platform-specific domain validation
- LinkedIn: must be linkedin.com domain
- GitHub: must be github.com domain
- Twitter: supports both twitter.com and x.com

### 9. Job Descriptions Schema (`app/features/job_descriptions/schemas.py`)

**Enhancements:**
- Comprehensive job posting information
- Skills and requirements extraction
- Employment type categorization
- Salary range parsing
- Location and company validation

**Key Validations:**
- Job title: 1-255 characters, non-empty
- Company: 1-255 characters, non-empty
- Content: max 50000 characters
- Requirements/skills: list validation with parsing
- URL: job site domain awareness

### 10. Resumes Schema (`app/features/resumes/schemas.py`)

**Enhancements:**
- Resume template validation
- Component type enumeration
- Relevance score validation
- Content structure validation
- Template-specific validation

**Key Validations:**
- Title: 1-255 characters, non-empty
- Template: predefined options (modern, classic, creative, minimal, professional)
- Relevance score: 0-100 range
- Component order: 0-100 range
- Content: structured JSON validation

## Common Validation Patterns

### Field Constraints
```python
# String fields with length constraints
field_name: str = Field(..., min_length=1, max_length=255, description="Field description")

# Numeric fields with range constraints
score: float = Field(..., ge=0.0, le=100.0, description="Score between 0 and 100")

# Optional fields with validation
optional_field: Optional[str] = Field(None, min_length=1, max_length=100)
```

### Custom Validators
```python
@validator('field_name')
def validate_field_name(cls, v):
    if not v.strip():
        raise ValueError('Field cannot be empty or whitespace only')
    return v.strip()
```

### Date Validation
```python
@validator('end_date')
def validate_end_date(cls, v, values):
    start_date = values.get('start_date')
    if start_date and v and v < start_date:
        raise ValueError('End date cannot be before start date')
    return v
```

### List Validation
```python
@validator('list_field', pre=True)
def validate_list_field(cls, v):
    if v is None:
        return []
    if isinstance(v, str):
        return [item.strip() for item in v.split(',') if item.strip()]
    return v
```

## Relationship Updates

All schemas have been updated to use the new hierarchical structure:

### Before (Flat Structure)
```python
class CreateSchema(BaseSchema):
    user_uuid: str  # Direct user reference
```

### After (Hierarchical Structure)
```python
class CreateSchema(BaseSchema):
    profile_id: int = Field(..., ge=1, description="ID of the profile this belongs to")
```

## Error Handling Improvements

### Validation Error Messages
- Clear, user-friendly error messages
- Specific field validation failures
- Business logic validation errors
- Type conversion error handling

### Example Error Response
```json
{
    "detail": [
        {
            "loc": ["body", "company_name"],
            "msg": "Company name cannot be empty or whitespace only",
            "type": "value_error"
        },
        {
            "loc": ["body", "salary"],
            "msg": "Salary must be a non-negative number",
            "type": "value_error"
        }
    ]
}
```

## Documentation Improvements

Each schema field now includes:
- Clear description of the field purpose
- Validation constraints explanation
- Example values where appropriate
- Relationship information
- Business rule documentation

## Testing Considerations

The enhanced schemas provide better validation coverage for:
- Input sanitization
- Business rule enforcement
- Data integrity checks
- API contract validation
- Error handling scenarios

## Performance Impact

The validation enhancements have minimal performance impact:
- Field validation is fast and efficient
- Custom validators only run when needed
- Pre-validation transformations optimize data processing
- Caching of validation results where possible

## Migration Notes

For existing data:
1. Most validations are additive and won't break existing records
2. New required fields have sensible defaults
3. Field length constraints are generous to accommodate existing data
4. Date validation only applies to new/updated records

## Future Enhancements

Potential future improvements:
1. Async validators for database lookups
2. Cross-field validation rules
3. Dynamic validation based on user preferences
4. Internationalization support for error messages
5. Custom validation decorators for common patterns
