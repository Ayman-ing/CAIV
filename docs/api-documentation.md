# API Documentation

## Overview

The AI Resume Builder API follows RESTful principles with a feature-based architecture. Each feature module contains models, schemas, repositories, services, and routers following the Repository-Service-Router pattern.

## Authentication

The API uses UUID-based public identifiers for all external access, keeping internal database IDs private for security.

## Base URL

```
http://localhost:8000/api/v1
```

## Response Format

All API responses follow a consistent format:

```json
{
  "success": true,
  "data": {},
  "message": "Success message",
  "errors": []
}
```

## API Endpoints

### User Management

#### Create User
```http
POST /users
```

**Request Body:**
```json
{
  "email": "user@example.com",
  "location": "New York, NY",
  "phone_number": "+1-555-0123"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "uuid": "123e4567-e89b-12d3-a456-426614174000",
    "email": "user@example.com",
    "location": "New York, NY",
    "phone_number": "+1-555-0123",
    "created_at": "2025-08-08T15:30:00Z"
  },
  "message": "User created successfully"
}
```

#### Get User
```http
GET /users/{user_uuid}
```

#### Update User
```http
PUT /users/{user_uuid}
```

#### Delete User
```http
DELETE /users/{user_uuid}
```

### Profile Management

#### Create Profile
```http
POST /profiles
```

**Request Body:**
```json
{
  "user_uuid": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Software Engineer Profile"
}
```

#### Get User Profiles
```http
GET /users/{user_uuid}/profiles
```

#### Get Profile
```http
GET /profiles/{profile_uuid}
```

#### Update Profile
```http
PUT /profiles/{profile_uuid}
```

#### Delete Profile
```http
DELETE /profiles/{profile_uuid}
```

### Education Management

#### Add Education
```http
POST /profiles/{profile_uuid}/education
```

**Request Body:**
```json
{
  "institution": "University of Technology",
  "degree": "Bachelor of Science",
  "field_of_study": "Computer Science",
  "start_date": "2018-09-01",
  "end_date": "2022-05-15",
  "gpa": "3.8"
}
```

#### Get Profile Education
```http
GET /profiles/{profile_uuid}/education
```

#### Update Education
```http
PUT /education/{education_uuid}
```

#### Delete Education
```http
DELETE /education/{education_uuid}
```

### Work Experience Management

#### Add Work Experience
```http
POST /profiles/{profile_uuid}/work-experiences
```

**Request Body:**
```json
{
  "company": "Tech Corp",
  "position": "Software Developer",
  "description": "Developed web applications using Python and React",
  "start_date": "2022-06-01",
  "end_date": null
}
```

#### Get Profile Work Experiences
```http
GET /profiles/{profile_uuid}/work-experiences
```

#### Update Work Experience
```http
PUT /work-experiences/{experience_uuid}
```

#### Delete Work Experience
```http
DELETE /work-experiences/{experience_uuid}
```

### Skills Management

#### Add Skill
```http
POST /profiles/{profile_uuid}/skills
```

**Request Body:**
```json
{
  "name": "Python",
  "category": "Programming Languages",
  "proficiency": "Advanced"
}
```

#### Get Profile Skills
```http
GET /profiles/{profile_uuid}/skills
```

#### Update Skill
```http
PUT /skills/{skill_uuid}
```

#### Delete Skill
```http
DELETE /skills/{skill_uuid}
```

### Projects Management

#### Add Project
```http
POST /profiles/{profile_uuid}/projects
```

**Request Body:**
```json
{
  "name": "E-commerce Platform",
  "description": "Full-stack e-commerce application with payment processing",
  "technologies": "Python, FastAPI, React, PostgreSQL",
  "start_date": "2023-01-01",
  "end_date": "2023-06-01",
  "url": "https://github.com/user/ecommerce-platform"
}
```

#### Get Profile Projects
```http
GET /profiles/{profile_uuid}/projects
```

#### Update Project
```http
PUT /projects/{project_uuid}
```

#### Delete Project
```http
DELETE /projects/{project_uuid}
```

### Certificates Management

#### Add Certificate
```http
POST /profiles/{profile_uuid}/certificates
```

**Request Body:**
```json
{
  "name": "AWS Certified Solutions Architect",
  "issuing_organization": "Amazon Web Services",
  "issue_date": "2023-03-15",
  "expiration_date": "2026-03-15",
  "credential_id": "AWS-CSA-12345"
}
```

#### Get Profile Certificates
```http
GET /profiles/{profile_uuid}/certificates
```

#### Update Certificate
```http
PUT /certificates/{certificate_uuid}
```

#### Delete Certificate
```http
DELETE /certificates/{certificate_uuid}
```

### Languages Management

#### Add Language
```http
POST /profiles/{profile_uuid}/languages
```

**Request Body:**
```json
{
  "language": "Spanish",
  "proficiency": "Conversational"
}
```

#### Get Profile Languages
```http
GET /profiles/{profile_uuid}/languages
```

#### Update Language
```http
PUT /languages/{language_uuid}
```

#### Delete Language
```http
DELETE /languages/{language_uuid}
```

### Professional Summaries Management

#### Add Professional Summary
```http
POST /profiles/{profile_uuid}/professional-summaries
```

**Request Body:**
```json
{
  "title": "Software Engineer Summary",
  "content": "Experienced software engineer with 5+ years developing scalable web applications..."
}
```

#### Get Profile Professional Summaries
```http
GET /profiles/{profile_uuid}/professional-summaries
```

#### Update Professional Summary
```http
PUT /professional-summaries/{summary_uuid}
```

#### Delete Professional Summary
```http
DELETE /professional-summaries/{summary_uuid}
```

### Profile Links Management

#### Add Profile Link
```http
POST /profiles/{profile_uuid}/profile-links
```

**Request Body:**
```json
{
  "platform": "LinkedIn",
  "url": "https://linkedin.com/in/johndoe"
}
```

#### Get Profile Links
```http
GET /profiles/{profile_uuid}/profile-links
```

#### Update Profile Link
```http
PUT /profile-links/{link_uuid}
```

#### Delete Profile Link
```http
DELETE /profile-links/{link_uuid}
```

### Custom Sections Management

#### Add Custom Section
```http
POST /profiles/{profile_uuid}/custom-sections
```

**Request Body:**
```json
{
  "title": "Volunteer Work",
  "content": "Local coding bootcamp mentor, helping students learn programming fundamentals"
}
```

#### Get Profile Custom Sections
```http
GET /profiles/{profile_uuid}/custom-sections
```

#### Update Custom Section
```http
PUT /custom-sections/{section_uuid}
```

#### Delete Custom Section
```http
DELETE /custom-sections/{section_uuid}
```

### Job Descriptions Management

#### Create Job Description
```http
POST /job-descriptions
```

**Request Body:**
```json
{
  "user_uuid": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Senior Software Engineer",
  "company": "TechCorp Inc.",
  "description": "We are looking for a senior software engineer to join our team..."
}
```

#### Get User Job Descriptions
```http
GET /users/{user_uuid}/job-descriptions
```

#### Get Job Description
```http
GET /job-descriptions/{job_description_uuid}
```

#### Update Job Description
```http
PUT /job-descriptions/{job_description_uuid}
```

#### Delete Job Description
```http
DELETE /job-descriptions/{job_description_uuid}
```

### Resume Generation

#### Generate Resume
```http
POST /resumes/generate
```

**Request Body:**
```json
{
  "profile_uuid": "123e4567-e89b-12d3-a456-426614174000",
  "job_description_uuid": "456e7890-e89b-12d3-a456-426614174001",
  "title": "Software Engineer Resume for TechCorp",
  "format": "pdf"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "uuid": "789e0123-e89b-12d3-a456-426614174002",
    "title": "Software Engineer Resume for TechCorp",
    "content": "Generated resume content...",
    "format": "pdf",
    "created_at": "2025-08-08T15:30:00Z"
  },
  "message": "Resume generated successfully"
}
```

#### Get Profile Resumes
```http
GET /profiles/{profile_uuid}/resumes
```

#### Get Resume
```http
GET /resumes/{resume_uuid}
```

#### Update Resume
```http
PUT /resumes/{resume_uuid}
```

#### Delete Resume
```http
DELETE /resumes/{resume_uuid}
```

#### Download Resume
```http
GET /resumes/{resume_uuid}/download
```

### AI-Powered Features

#### Analyze Job Description
```http
POST /job-descriptions/{job_description_uuid}/analyze
```

**Response:**
```json
{
  "success": true,
  "data": {
    "keywords": [
      {"keyword": "Python", "importance_score": 0.95},
      {"keyword": "FastAPI", "importance_score": 0.87}
    ],
    "requirements": [
      {
        "requirement_type": "skill",
        "description": "5+ years Python experience",
        "is_required": true
      }
    ]
  },
  "message": "Job description analyzed successfully"
}
```

#### Match Profile to Job
```http
POST /profiles/{profile_uuid}/match-job
```

**Request Body:**
```json
{
  "job_description_uuid": "456e7890-e89b-12d3-a456-426614174001"
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "match_score": 0.87,
    "matching_skills": ["Python", "FastAPI", "PostgreSQL"],
    "missing_skills": ["Docker", "Kubernetes"],
    "recommendations": [
      "Add Docker experience to your skills",
      "Highlight FastAPI projects in your experience section"
    ]
  },
  "message": "Profile matched to job successfully"
}
```

#### Optimize Resume Content
```http
POST /resumes/{resume_uuid}/optimize
```

**Request Body:**
```json
{
  "job_description_uuid": "456e7890-e89b-12d3-a456-426614174001"
}
```

## Error Handling

### Error Response Format

```json
{
  "success": false,
  "data": null,
  "message": "Error message",
  "errors": [
    {
      "field": "email",
      "code": "INVALID_EMAIL",
      "message": "Please provide a valid email address"
    }
  ]
}
```

### HTTP Status Codes

- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Invalid request data
- `401 Unauthorized` - Authentication required
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation errors
- `500 Internal Server Error` - Server error

### Common Error Codes

- `VALIDATION_ERROR` - Request validation failed
- `NOT_FOUND` - Resource not found
- `DUPLICATE_RESOURCE` - Resource already exists
- `FOREIGN_KEY_VIOLATION` - Referenced resource doesn't exist
- `PERMISSION_DENIED` - Insufficient permissions
- `RATE_LIMIT_EXCEEDED` - Too many requests

## Rate Limiting

API requests are rate-limited to prevent abuse:

- **Standard endpoints**: 100 requests per minute
- **AI-powered endpoints**: 20 requests per minute
- **File uploads**: 10 requests per minute

Rate limit headers are included in responses:

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1625097600
```

## Pagination

List endpoints support pagination with query parameters:

```http
GET /profiles/{profile_uuid}/work-experiences?page=1&size=10&sort=start_date&order=desc
```

**Parameters:**
- `page` - Page number (default: 1)
- `size` - Items per page (default: 20, max: 100)
- `sort` - Sort field (default: created_at)
- `order` - Sort order: asc, desc (default: desc)

**Response:**
```json
{
  "success": true,
  "data": {
    "items": [...],
    "pagination": {
      "page": 1,
      "size": 10,
      "total": 25,
      "pages": 3,
      "has_next": true,
      "has_prev": false
    }
  }
}
```

## Search and Filtering

Many endpoints support search and filtering:

```http
GET /profiles/{profile_uuid}/skills?search=python&category=programming
```

**Common filters:**
- `search` - Text search across relevant fields
- `created_after` - Filter by creation date
- `updated_after` - Filter by update date
- Custom filters per resource type

## Webhooks (Future Feature)

The API will support webhooks for real-time notifications:

- Resume generation completed
- AI analysis completed
- Profile updated
- New job match found

## SDK and Libraries

Official SDKs will be available for:

- Python
- JavaScript/TypeScript
- React
- Mobile (React Native)

## OpenAPI Documentation

Interactive API documentation is available at:

```
http://localhost:8000/docs
```

Alternative documentation format:

```
http://localhost:8000/redoc
```
