import uuid
import requests

test_uuid = uuid.uuid4()
url = "http://127.0.0.1:8081"
email = f"test_{test_uuid}@gmail.com"
password = f"testpwd_{test_uuid}"
full_name = "Test User"

def register_user():
    response = requests.post(f"{url}/auth/register?email={email}&password={password}&full_name={full_name}")
    
    assert response.status_code == 200
    assert response.json().get("message") == "User registered successfully"

def login_user():
    response = requests.post(f"{url}/auth/login?email={email}&password={password}")
    
    assert response.status_code == 200
    assert "access_token" in response.json()

    token = response.json().get("access_token")

    return token

def draw_card():
    response = requests.get(f"{url}/cards/draw?token={token}")
    
    assert response.status_code == 200
    assert "id" in response.json()

    return response.json()

def check_card_in_inventory(card_id):
    response = requests.get(f"{url}/cards/inventory?token={token}&card_id={card_id}")
    
    assert response.status_code == 200
    assert "cards" in response.json()

def get_card_info(card_id):
    response = requests.get(f"{url}/cards/info?card_id={card_id}")
    
    assert response.status_code == 200
    assert "id" in response.json()


if __name__ == "__main__":
    print("Starting tests...")
    print(f"Test url: {url}")
    print(f"Test uuid: {test_uuid}")
    print(f"Test email: {email}")
    print(f"Test password: {password}")
    print(f"Test full name: {full_name}")

    register_user()
    token = login_user()
    card = draw_card()
    check_card_in_inventory(card.id)
    get_card_info(card.id)

    print("Ok!")