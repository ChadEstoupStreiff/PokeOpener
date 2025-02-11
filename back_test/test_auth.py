import uuid

import requests

test_uuid = uuid.uuid4()
url = "http://127.0.0.1:8081"
email = f"test_{test_uuid}@gmail.com"
password = f"testpwd_{test_uuid}"
full_name = "Test User"
token = None
card_id = None


##############
# Auth tests #
##############


def test_url():
    response = requests.get(f"{url}/docs")

    assert response.status_code == 200


def test_register():
    response = requests.post(
        f"{url}/auth/register?email={email}&password={password}&full_name={full_name}"
    )

    assert response.status_code == 200
    assert response.json().get("message") == "User registered successfully"


def test_cant_register_same_email():
    response = requests.post(
        f"{url}/auth/register?email={email}&password={password}&full_name={full_name}"
    )

    assert response.status_code == 400
    assert response.json().get("detail") == "Email already registered"


def test_login():
    response = requests.post(f"{url}/auth/login?email={email}&password={password}")

    assert response.status_code == 200
    assert "access_token" in response.json()

    global token
    token = response.json().get("access_token")


def test_cant_login_wrong_password():
    response = requests.post(
        f"{url}/auth/login?email={email}&password={password[::-1]}"
    )

    assert response.status_code == 400
    assert response.json().get("detail") == "Invalid credentials"


def test_cant_login_wrong_email():
    response = requests.post(
        f"{url}/auth/login?email={email[::-1]}&password={password}"
    )

    assert response.status_code == 400
    assert response.json().get("detail") == "Invalid credentials"


def test_token_validity():
    response = requests.get(f"{url}/auth/info?token={token}")

    assert response.status_code == 200
    assert "user_id" in response.json()
    assert "email" in response.json()
    assert "full_name" in response.json()


###############
# Cards tests #
###############


def test_draw_card():
    response = requests.get(f"{url}/cards/draw?token={token}")

    assert response.status_code == 200
    assert "id" in response.json()

    global card_id
    card_id = response.json().get("id")


def test_check_card_in_inventory():
    response = requests.get(f"{url}/cards/inventory?token={token}")

    assert response.status_code == 200
    assert any(card["card_id"] == card_id for card in response.json())


def test_get_card_info():
    response = requests.get(f"{url}/cards/get?card_id={card_id}")

    assert response.status_code == 200
    assert "id" in response.json()
