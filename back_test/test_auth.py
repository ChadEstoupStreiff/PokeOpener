import requests
import random
import string
import uuid
import time

test_uuid = uuid.uuid4()
url = "http://localhost:8081"
email = f"test_{test_uuid}@gmail.com"
password = f"testpwd_{test_uuid}"
full_name = "Test User"

def test_url():
    for _ in range(20):
        response = requests.get(f"{url}/docs")
        
        if response.status_code == 200:
            break
        
        time.sleep(5)
    
    assert response.status_code == 200

def test_register():
    
    response = requests.post(f"{url}/auth/register?email={email}&password={password}&full_name={full_name}")
    
    assert response.status_code == 200
    assert response.json().get("message") == "User registered successfully"

def test_cant_register_same_email():
    
    response = requests.post(f"{url}/auth/register?email={email}&password={password}&full_name={full_name}")
    
    assert response.status_code == 400
    assert response.json().get("detail") == "Email already registered"


def test_login():
    
    response = requests.post(f"{url}/auth/login?email={email}&password={password}")
    
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_cant_login_wrong_password():
    
    response = requests.post(f"{url}/auth/login?email={email}&password={password[::-1]}")
    
    assert response.status_code == 400
    assert response.json().get("detail") == "Invalid credentials"

def test_cant_login_wrong_email():
    
    response = requests.post(f"{url}/auth/login?email={email[::-1]}&password={password}")
    
    assert response.status_code == 400
    assert response.json().get("detail") == "Invalid credentials"

def test_token_validity():
    
    response = requests.post(f"{url}/auth/login?email={email}&password={password}")
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    
    token = response.json().get("access_token")
    
    response = requests.get(f"{url}/auth/info?token={token}")
    
    assert response.status_code == 200
    assert "user_id" in response.json()
    assert "email" in response.json()
    assert "full_name" in response.json()

if __name__ == "__main__":
    print("Starting tests...")
    print(f"Test url: {url}")
    print(f"Test uuid: {test_uuid}")
    print(f"Test email: {email}")
    print(f"Test password: {password}")
    print(f"Test full name: {full_name}")

    test_url()
    test_register()
    test_cant_register_same_email()
    test_login()
    test_cant_login_wrong_password()
    test_cant_login_wrong_email()
    test_token_validity()

    print("Ok!")