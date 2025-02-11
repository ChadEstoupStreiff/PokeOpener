import uuid

import requests
import logging

test_uuid = uuid.uuid4()
url = "http://127.0.0.1:8081"
email = f"test_{test_uuid}@gmail.com"
password = f"testpwd_{test_uuid}"
full_name = "Test User"


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
    response = requests.post(f"{url}/auth/login?email={email}&password={password}")

    assert response.status_code == 200
    assert "access_token" in response.json()

    token = response.json().get("access_token")

    response = requests.get(f"{url}/auth/info?token={token}")

    assert response.status_code == 200
    assert "user_id" in response.json()
    assert "email" in response.json()
    assert "full_name" in response.json()


def register_user():
    response = requests.post(
        f"{url}/auth/register?email={email}&password={password}&full_name={full_name}"
    )

    assert response.status_code == 200
    assert response.json().get("message") == "User registered successfully"


def login_user():
    response = requests.post(f"{url}/auth/login?email={email}&password={password}")

    assert response.status_code == 200
    assert "access_token" in response.json()

    token = response.json().get("access_token")

    return token


def test_draw_card(token):
    response = requests.get(f"{url}/cards/draw?token={token}")

    assert response.status_code == 200
    assert "id" in response.json()

    return response.json()


def test_check_card_in_inventory(token, card_id):
    response = requests.get(f"{url}/cards/inventory?token={token}")

    assert response.status_code == 200
    assert card_id in response.json()


def test_get_card_info(token, card_id):
    response = requests.get(f"{url}/cards/get?card_id={card_id}")

    assert response.status_code == 200
    assert "id" in response.json()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    logging.info("Starting tests...")
    logging.info(f"Test url: {url}")
    logging.info(f"Test uuid: {test_uuid}")
    logging.info(f"Test email: {email}")
    logging.info(f"Test password: {password}")
    logging.info(f"Test full name: {full_name}")

    test_url()
    test_register()
    test_cant_register_same_email()
    test_login()
    test_cant_login_wrong_password()
    test_cant_login_wrong_email()
    test_token_validity()

    test_uuid = uuid.uuid4()
    url = "http://127.0.0.1:8081"
    email = f"test_{test_uuid}@gmail.com"
    password = f"testpwd_{test_uuid}"
    full_name = "Test User"
    logging.info(f"Test url: {url}")
    logging.info(f"Test uuid: {test_uuid}")
    logging.info(f"Test email: {email}")
    logging.info(f"Test password: {password}")
    logging.info(f"Test full name: {full_name}")

    register_user()
    token = login_user()
    card = test_draw_card(token)
    test_check_card_in_inventory(token, card.id)
    test_get_card_info(token, card.id)

    logging.info("Ok!")
