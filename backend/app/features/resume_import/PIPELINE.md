# Resume Import Pipeline

## Overview
The resume import pipeline automates the extraction of structured profile data from PDF resumes. It uses:
- **Docling** - PDF text extraction with advanced document parsing
- **LLM (Groq/Claude)** - Intelligent data structuring and categorization
- **Database** - Persistent storage of extracted profile data

## Pipeline Flow

### 1. File Upload (`POST /api/v1/resume-import/upload`)
```
User uploads PDF
    ↓
Router validates file (pdf_parser_service.py)
    ↓
Service.upload_and_parse_resume() [ASYNC]
```

### 2. Text Extraction
```
PDFParserService.parse_cv_structure()
    ↓
Docling extracts PDF → Markdown text
```

### 3. LLM Parsing (Main Intelligence)
```
LLMService.parse_to_model()
    ↓
Groq API processes text with ResumeData schema
    ↓
Returns JSON matching profile schemas
```

**Key Instructions sent to LLM:**
- Extract contact info (name, email, phone, location)
- Identify and structure: education, work experience, skills, projects, certificates, languages
- **Custom Sections** - For data that doesn't fit standard categories
- Format dates as YYYY-MM-DD or YYYY
- Map proficiency levels to enum values

### 4. Database Population
```
Extracted JSON
    ↓
Map to profile sub-repositories:
  - Education
  - WorkExperience
  - Skills
  - Certificates
  - Languages
  - Projects
  - ProfessionalSummaries
  - CustomSections
    ↓
Create entries in database
```

## Data Schema

### Input: Resume PDF → Output: ResumeData Model

```python
class ResumeData:
    contact_info: ContactInfo
    professional_summaries: List[ProfessionalSummaryCreate]
    education: List[EducationCreate]
    work_experiences: List[WorkExperienceCreate]
    skills: List[SkillCreate]
    projects: List[ProjectCreate]
    certificates: List[CertificateCreate]
    languages: List[LanguageCreate]
    custom_sections: List[CustomSectionCreate]  # Catch-all for unstructured data
```

## Custom Sections Strategy

The **custom_sections** field serves as a fallback for any content that cannot be categorized into standard sections. This ensures no information is lost during parsing.

Examples:
- "Volunteer Experience"
- "Publications"
- "Awards & Recognition"
- "Technical Publications"
- "Hobbies & Interests"

## Async Architecture

All operations are async-compatible:
- `LLMService.parse_to_model()` - Async
- `PDFParserService.parse_cv_structure()` - Async
- `ResumeImportService.upload_and_parse_resume()` - Async
- Router endpoint - Async

This enables concurrent processing without blocking other requests.

## Error Handling

1. **File Validation** - Checked in dependencies.py
2. **Profile Ownership** - Verified before processing
3. **LLM Parsing Failures** - Returns empty structure, logs warning
4. **Database Errors** - Per-entry error handling doesn't stop other entries
5. **Malformed Dates/Numbers** - Safe parsing with None defaults

## Files Modified

- `backend/app/features/resume_import/service.py` - Fixed structure, made async
- `backend/app/features/resume_import/router.py` - Made endpoint async
- `backend/app/features/resume_import/pdf_parser_service.py` - Made async
- `backend/app/features/llm/service.py` - Removed duplicate API call

## Testing the Pipeline

### Setup
1. Ensure `GROQ_API_KEY` environment variable is set
2. Create a profile via Dashboard or API
3. Get profile UUID

### Test Upload
```bash
curl -X POST http://localhost:8000/api/v1/resume-import/upload \
  -F "resume=@sample.pdf" \
  -F "profile_id={profile_uuid}" \
  -H "Authorization: Bearer {jwt_token}"
```

### Check Status
```bash
GET http://localhost:8000/api/v1/resume-import/status/{resume_id}
```

### Confirm Import
```bash
POST http://localhost:8000/api/v1/resume-import/confirm \
  -H "Content-Type: application/json" \
  -d '{
    "resume_id": "{resume_id}",
    "confirm": true
  }'
```

## Future Enhancements

1. **Multiple File Formats** - Support DOCX, TXT alongside PDF
2. **Batch Processing** - Upload multiple resumes
3. **Manual Override** - User can correct extracted data before confirming
4. **Confidence Scores** - LLM returns confidence for each extracted field
5. **Template Matching** - Detect and use resume format templates
