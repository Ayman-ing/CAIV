import httpx
import uuid
import sys

BASE_URL = "http://localhost:8000/api/v1"

def test_flow():
    try:
        with httpx.Client(base_url=BASE_URL) as client:
            # 1. Register
            email = f"test_{uuid.uuid4().hex[:8]}@example.com"
            password = "Password123!"
            print(f"Registering user {email}...")
            resp = client.post("/auth/register", json={
                "email": email,
                "password": password,
                "confirm_password": password,
                "first_name": "Test",
                "last_name": "User"
            })
            print("Register response:", resp.status_code, resp.text)
            if resp.status_code != 201:
                print("Registration failed!")
                sys.exit(1)
            
            user_uuid = resp.json()["user_id"]
            
            # 2. Login
            print("\nLogging in...")
            resp = client.post("/auth/login", data={"username": email, "password": password})
            print("Login response:", resp.status_code)
            if resp.status_code != 200:
                print("Login failed!")
                sys.exit(1)
            token = resp.json()["access_token"]
            headers = {"Authorization": f"Bearer {token}"}
            
            # 3. Create Profile
            print("\nCreating profile...")
            resp = client.post(f"/profiles/?user_uuid={user_uuid}", json={
                "name": "Test User",
                "headline": "Software Engineer"
            }, headers=headers)
            print("Create Profile response:", resp.status_code, resp.text)
            if resp.status_code != 201:
                print("Profile creation failed!")
                sys.exit(1)
            profile_uuid = resp.json()["uuid"]
            
            # 4. Get Profile
            print("\nGetting profile...")
            resp = client.get(f"/profiles/{profile_uuid}?user_uuid={user_uuid}", headers=headers)
            print("Get Profile response:", resp.status_code, resp.text)
            if resp.status_code != 200:
                print("Get profile failed!")
                sys.exit(1)
            
            # 5. Update Profile
            print("\nUpdating profile...")
            resp = client.put(f"/profiles/{profile_uuid}?user_uuid={user_uuid}", json={
                "headline": "Senior Software Engineer"
            }, headers=headers)
            print("Update Profile response:", resp.status_code, resp.text)
            if resp.status_code != 200:
                print("Update profile failed!")
                sys.exit(1)
            
            # 6. Delete Profile
            print("\nDeleting profile...")
            resp = client.delete(f"/profiles/{profile_uuid}?user_uuid={user_uuid}", headers=headers)
            print("Delete Profile response:", resp.status_code, resp.text)
            if resp.status_code != 200:
                print("Delete profile failed!")
                sys.exit(1)
            
            print("\n✅ ALL TESTS PASSED!")
    except Exception as e:
        print(f"Test failed with exception: {e}")
        sys.exit(1)

if __name__ == "__main__":
    test_flow()
