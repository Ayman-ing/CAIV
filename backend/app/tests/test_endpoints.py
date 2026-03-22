"""
Comprehensive endpoint tests for all profile sections.
Tests cover complete CRUD operations and validation.
Run with: pytest tests/test_endpoints.py -v
"""

import pytest
import httpx
import uuid
from typing import Tuple

BASE_URL = "http://localhost:8000/api/v1"


@pytest.fixture
def auth_client() -> Tuple[httpx.Client, str, str]:
    """Create authenticated client with profile"""
    client = httpx.Client(base_url=BASE_URL)
    
    # Register (profile is auto-created)
    email = f"test_{uuid.uuid4().hex[:8]}@example.com"
    password = "TestPass123!"
    
    resp = client.post("/auth/register", json={
        "email": email,
        "password": password,
        "confirm_password": password,
        "first_name": "Test",
        "last_name": "User"
    })
    assert resp.status_code == 201
    user_uuid = resp.json()["user_id"]
    token = resp.json()["access_token"]
    
    # Get auto-created profile
    resp = client.get(f"/profiles/?user_uuid={user_uuid}", headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code == 200
    profiles = resp.json()
    assert len(profiles) > 0
    profile_uuid = profiles[0]["uuid"]
    
    yield client, token, profile_uuid
    client.close()


class TestLanguageCRUD:
    """Complete CRUD tests for Languages endpoint"""
    
    def test_01_create_language(self, auth_client):
        """CREATE: Add a new language"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        resp = client.post(
            f"/profiles/{profile_uuid}/languages/",
            json={
                "language": "English",
                "proficiency": "Native",
                "can_read": True,
                "can_write": True,
                "can_speak": True
            },
            headers=headers
        )
        
        assert resp.status_code == 201, f"Create failed: {resp.text}"
        data = resp.json()
        assert data["language"] == "English"
        assert data["proficiency"] == "Native"
        assert "uuid" in data
        assert "created_at" in data
    
    def test_02_read_all_languages(self, auth_client):
        """READ: Get all languages"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        # Add multiple languages
        client.post(
            f"/profiles/{profile_uuid}/languages/",
            json={"language": "French", "proficiency": "Fluent"},
            headers=headers
        )
        client.post(
            f"/profiles/{profile_uuid}/languages/",
            json={"language": "Spanish", "proficiency": "Conversational"},
            headers=headers
        )
        
        resp = client.get(f"/profiles/{profile_uuid}/languages/", headers=headers)
        
        assert resp.status_code == 200
        languages = resp.json()
        assert len(languages) >= 2
        assert any(l["language"] == "French" for l in languages)
        assert any(l["language"] == "Spanish" for l in languages)
    
    def test_03_update_language(self, auth_client):
        """UPDATE: Modify language proficiency"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create language
        create_resp = client.post(
            f"/profiles/{profile_uuid}/languages/",
            json={"language": "German", "proficiency": "Basic"},
            headers=headers
        )
        language_uuid = create_resp.json()["uuid"]
        
        # Update it
        resp = client.put(
            f"/profiles/{profile_uuid}/languages/{language_uuid}",
            json={
                "proficiency": "Intermediate",
                "can_speak": False
            },
            headers=headers
        )
        
        assert resp.status_code == 200
        data = resp.json()
        assert data["proficiency"] == "Intermediate"
        assert data["can_speak"] == False
    
    def test_04_delete_language(self, auth_client):
        """DELETE: Remove a language"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create language
        create_resp = client.post(
            f"/profiles/{profile_uuid}/languages/",
            json={"language": "Portuguese", "proficiency": "Basic"},
            headers=headers
        )
        language_uuid = create_resp.json()["uuid"]
        
        # Delete it
        resp = client.delete(
            f"/profiles/{profile_uuid}/languages/{language_uuid}",
            headers=headers
        )
        
        assert resp.status_code == 204
        
        # Verify it's deleted by checking list
        get_resp = client.get(f"/profiles/{profile_uuid}/languages/", headers=headers)
        assert get_resp.status_code == 200
        languages = get_resp.json()
        assert not any(l["uuid"] == str(language_uuid) for l in languages)
    
    def test_05_duplicate_prevention(self, auth_client):
        """VALIDATION: Prevent duplicate languages"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        # Add first
        resp1 = client.post(
            f"/profiles/{profile_uuid}/languages/",
            json={"language": "Russian", "proficiency": "Intermediate"},
            headers=headers
        )
        assert resp1.status_code == 201
        
        # Try duplicate
        resp2 = client.post(
            f"/profiles/{profile_uuid}/languages/",
            json={"language": "Russian", "proficiency": "Fluent"},
            headers=headers
        )
        assert resp2.status_code == 400
        assert "exists" in resp2.text.lower() or "duplicate" in resp2.text.lower()


class TestSkillsCRUD:
    """Complete CRUD tests for Skills endpoint"""
    
    def test_01_create_skill(self, auth_client):
        """CREATE: Add a new skill"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        resp = client.post(
            f"/profiles/{profile_uuid}/skills/",
            json={
                "category": "Programming",
                "name": "Python",
                "proficiency": "Expert",
                "years_experience": 5
            },
            headers=headers
        )
        
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "Python"
        assert data["proficiency"] == "Expert"
        assert data["years_experience"] == 5
    
    def test_02_read_all_skills(self, auth_client):
        """READ: Get all skills"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        # Add skills
        client.post(
            f"/profiles/{profile_uuid}/skills/",
            json={"category": "Programming", "name": "JavaScript", "proficiency": "Advanced"},
            headers=headers
        )
        client.post(
            f"/profiles/{profile_uuid}/skills/",
            json={"category": "Frontend", "name": "React", "proficiency": "Advanced"},
            headers=headers
        )
        
        resp = client.get(f"/profiles/{profile_uuid}/skills/", headers=headers)
        
        assert resp.status_code == 200
        skills = resp.json()
        assert len(skills) >= 2
    
    def test_03_update_skill(self, auth_client):
        """UPDATE: Modify skill proficiency"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create skill
        create_resp = client.post(
            f"/profiles/{profile_uuid}/skills/",
            json={"category": "Frontend", "name": "Vue", "proficiency": "Intermediate", "years_experience": 2},
            headers=headers
        )
        skill_uuid = create_resp.json()["uuid"]
        
        # Update it
        resp = client.put(
            f"/profiles/{profile_uuid}/skills/{skill_uuid}",
            json={
                "proficiency": "Expert",
                "years_experience": 4
            },
            headers=headers
        )
        
        assert resp.status_code == 200
        data = resp.json()
        assert data["proficiency"] == "Expert"
        assert data["years_experience"] == 4
    
    def test_04_delete_skill(self, auth_client):
        """DELETE: Remove a skill"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create skill
        create_resp = client.post(
            f"/profiles/{profile_uuid}/skills/",
            json={"category": "DevOps", "name": "Docker", "proficiency": "Intermediate"},
            headers=headers
        )
        skill_uuid = create_resp.json()["uuid"]
        
        # Delete it
        resp = client.delete(
            f"/profiles/{profile_uuid}/skills/{skill_uuid}",
            headers=headers
        )
        
        assert resp.status_code == 204


class TestEducationCRUD:
    """Complete CRUD tests for Education endpoint"""
    
    def test_01_create_education(self, auth_client):
        """CREATE: Add education record"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        resp = client.post(
            f"/profiles/{profile_uuid}/education/",
            json={
                "institution": "MIT",
                "degree": "Bachelor's",
                "field_of_study": "Computer Science",
                "start_date": "2018-09-01",
                "end_date": "2022-05-31",
                "gpa": 3.8
            },
            headers=headers
        )
        
        assert resp.status_code == 201
        data = resp.json()
        assert data["institution"] == "MIT"
        assert data["gpa"] == 3.8
    
    def test_02_read_all_education(self, auth_client):
        """READ: Get all education records"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        # Add records
        client.post(
            f"/profiles/{profile_uuid}/education/",
            json={
                "institution": "Stanford",
                "degree": "Master's",
                "field_of_study": "AI",
                "start_date": "2022-09-01",
                "end_date": "2024-05-31",
                "gpa": 4.0
            },
            headers=headers
        )
        
        resp = client.get(f"/profiles/{profile_uuid}/education/", headers=headers)
        
        assert resp.status_code == 200
        education = resp.json()
        assert len(education) >= 1
    
    def test_03_update_education(self, auth_client):
        """UPDATE: Modify education record"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create
        create_resp = client.post(
            f"/profiles/{profile_uuid}/education/",
            json={
                "institution": "Harvard",
                "degree": "Bachelor's",
                "field_of_study": "Engineering",
                "start_date": "2019-09-01",
                "end_date": "2023-05-31",
                "gpa": 3.5
            },
            headers=headers
        )
        education_uuid = create_resp.json()["uuid"]
        
        # Update
        resp = client.put(
            f"/profiles/{profile_uuid}/education/{education_uuid}",
            json={"gpa": 3.9},
            headers=headers
        )
        
        assert resp.status_code == 200
        assert resp.json()["gpa"] == 3.9
    
    def test_04_delete_education(self, auth_client):
        """DELETE: Remove education record"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        # Create
        create_resp = client.post(
            f"/profiles/{profile_uuid}/education/",
            json={
                "institution": "Yale",
                "degree": "PhD",
                "field_of_study": "CS",
                "start_date": "2020-09-01",
                "end_date": "2025-05-31"
            },
            headers=headers
        )
        education_uuid = create_resp.json()["uuid"]
        
        # Delete
        resp = client.delete(
            f"/profiles/{profile_uuid}/education/{education_uuid}",
            headers=headers
        )
        
        assert resp.status_code == 204
    
    def test_05_gpa_validation(self, auth_client):
        """VALIDATION: GPA must be 0-20"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        # GPA > 20 should fail
        resp = client.post(
            f"/profiles/{profile_uuid}/education/",
            json={
                "institution": "Test",
                "degree": "Test",
                "field_of_study": "Test",
                "gpa": 25.0,
                "start_date": "2020-01-01",
                "end_date": "2024-01-01"
            },
            headers=headers
        )
        
        assert resp.status_code == 422



class TestProjectsCRUD:
    """Complete CRUD tests for Projects endpoint"""
    
    def test_01_create_project(self, auth_client):
        """CREATE: Add a project"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        resp = client.post(
            f"/profiles/{profile_uuid}/projects/",
            json={
                "name": "AI Resume Builder",
                "description": "AI-powered resume generation",
                "start_date": "2024-01-15",
                "end_date": "2024-06-30",
                "url": "https://github.com/example/resume-builder",
                "technologies": "Python,FastAPI,Vue"
            },
            headers=headers
        )
        
        assert resp.status_code == 201
        data = resp.json()
        assert data["name"] == "AI Resume Builder"
    
    def test_02_read_all_projects(self, auth_client):
        """READ: Get all projects"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        client.post(
            f"/profiles/{profile_uuid}/projects/",
            json={
                "name": "Chat App",
                "description": "Real-time chat",
                "start_date": "2023-06-01",
                "url": "https://github.com/example/chat",
                "technologies": "Node,Express,React"
            },
            headers=headers
        )
        
        resp = client.get(f"/profiles/{profile_uuid}/projects/", headers=headers)
        
        assert resp.status_code == 200
        assert len(resp.json()) >= 1
    
    def test_03_update_project(self, auth_client):
        """UPDATE: Modify project"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        create_resp = client.post(
            f"/profiles/{profile_uuid}/projects/",
            json={
                "name": "E-commerce",
                "description": "Online store",
                "start_date": "2023-01-10",
                "url": "https://github.com/example/store",
                "technologies": "Python,Django"
            },
            headers=headers
        )
        project_uuid = create_resp.json()["uuid"]
        
        resp = client.put(
            f"/profiles/{profile_uuid}/projects/{project_uuid}",
            json={"description": "Advanced e-commerce platform"},
            headers=headers
        )
        
        assert resp.status_code == 200
    
    def test_04_delete_project(self, auth_client):
        """DELETE: Remove project"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        create_resp = client.post(
            f"/profiles/{profile_uuid}/projects/",
            json={
                "name": "Blog",
                "description": "Blog platform",
                "start_date": "2023-03-15",
                "url": "https://github.com/example/blog",
                "technologies": "Next.js,MongoDB"
            },
            headers=headers
        )
        project_uuid = create_resp.json()["uuid"]
        
        resp = client.delete(
            f"/profiles/{profile_uuid}/projects/{project_uuid}",
            headers=headers
        )
        
        assert resp.status_code == 204


class TestProfessionalSummaryCRUD:
    """Complete CRUD tests for Professional Summary endpoint"""
    
    def test_01_create_summary(self, auth_client):
        """CREATE: Add professional summary"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        resp = client.post(
            f"/profiles/{profile_uuid}/professional-summaries/",
            json={
                "title": "Software Engineer",
                "content": "Experienced engineer with 5+ years in full-stack development"
            },
            headers=headers
        )
        
        assert resp.status_code == 201
        data = resp.json()
        assert data["title"] == "Software Engineer"
    
    def test_02_read_all_summaries(self, auth_client):
        """READ: Get all professional summaries"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        client.post(
            f"/profiles/{profile_uuid}/professional-summaries/",
            json={
                "title": "DevOps Engineer",
                "content": "Cloud infrastructure specialist"
            },
            headers=headers
        )
        
        resp = client.get(f"/profiles/{profile_uuid}/professional-summaries/", headers=headers)
        
        assert resp.status_code == 200
        assert len(resp.json()) >= 1
    
    def test_03_update_summary(self, auth_client):
        """UPDATE: Modify professional summary"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        create_resp = client.post(
            f"/profiles/{profile_uuid}/professional-summaries/",
            json={
                "title": "Product Manager",
                "content": "PM with background in tech"
            },
            headers=headers
        )
        summary_uuid = create_resp.json()["uuid"]
        
        resp = client.put(
            f"/profiles/{profile_uuid}/professional-summaries/{summary_uuid}",
            json={"content": "Senior PM with 10 years experience"},
            headers=headers
        )
        
        assert resp.status_code == 200
    
    def test_04_delete_summary(self, auth_client):
        """DELETE: Remove professional summary"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        create_resp = client.post(
            f"/profiles/{profile_uuid}/professional-summaries/",
            json={
                "title": "Data Scientist",
                "content": "ML specialist"
            },
            headers=headers
        )
        summary_uuid = create_resp.json()["uuid"]
        
        resp = client.delete(
            f"/profiles/{profile_uuid}/professional-summaries/{summary_uuid}",
            headers=headers
        )
        
        assert resp.status_code == 204


class TestProfileLinksCRUD:
    """Complete CRUD tests for Profile Links endpoint"""
    
    def test_01_create_link(self, auth_client):
        """CREATE: Add profile link"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        resp = client.post(
            f"/profiles/{profile_uuid}/links/",
            json={
                "label": "GitHub",
                "url": "https://github.com/example",
                "platform": "github",
                "is_visible": True
            },
            headers=headers
        )
        
        assert resp.status_code == 201
        data = resp.json()
        assert data["platform"] == "github"
    
    def test_02_read_all_links(self, auth_client):
        """READ: Get all profile links"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        client.post(
            f"/profiles/{profile_uuid}/links/",
            json={
                "label": "LinkedIn",
                "url": "https://linkedin.com/in/example",
                "platform": "linkedin",
                "is_visible": True
            },
            headers=headers
        )
        
        resp = client.get(f"/profiles/{profile_uuid}/links/", headers=headers)
        
        assert resp.status_code == 200
        assert len(resp.json()) >= 1
    
    def test_03_update_link(self, auth_client):
        """UPDATE: Modify profile link"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        create_resp = client.post(
            f"/profiles/{profile_uuid}/links/",
            json={
                "label": "Portfolio",
                "url": "https://example.com",
                "platform": "portfolio",
                "is_visible": True
            },
            headers=headers
        )
        link_uuid = create_resp.json()["uuid"]
        
        resp = client.put(
            f"/profiles/{profile_uuid}/links/{link_uuid}",
            json={"is_visible": False},
            headers=headers
        )
        
        assert resp.status_code == 200
    
    def test_04_delete_link(self, auth_client):
        """DELETE: Remove profile link"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        create_resp = client.post(
            f"/profiles/{profile_uuid}/links/",
            json={
                "label": "Twitter",
                "url": "https://twitter.com/example",
                "platform": "twitter",
                "is_visible": True
            },
            headers=headers
        )
        link_uuid = create_resp.json()["uuid"]
        
        resp = client.delete(
            f"/profiles/{profile_uuid}/links/{link_uuid}",
            headers=headers
        )
        
        assert resp.status_code == 204
    
    def test_05_url_validation(self, auth_client):
        """VALIDATION: URL must be valid"""
        client, token, profile_uuid = auth_client
        headers = {"Authorization": f"Bearer {token}"}
        
        resp = client.post(
            f"/profiles/{profile_uuid}/links/",
            json={
                "label": "Invalid",
                "url": "not-a-valid-url",
                "platform": "other"
            },
            headers=headers
        )
        
        assert resp.status_code == 422


if __name__ == "__main__":
    print("Run pytest tests/test_endpoints.py -v")
