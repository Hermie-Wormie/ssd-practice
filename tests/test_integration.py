import pytest
from app.app import app, verify_password


@pytest.fixture
def client():
    app.config["TESTING"] = True
    app.config["WTF_CSRF_ENABLED"] = False
    return app.test_client()


def test_rejects_short_password():
    assert not verify_password("Ab1!xyz")  # 7 chars

def test_rejects_common_password():
    assert not verify_password("password")
    assert not verify_password("liverpool")

def test_accepts_strong_password():
    assert verify_password("correct horse battery staple 88")

def test_rejects_none():
    assert not verify_password(None)

def test_home_page_has_form(client):
    r = client.get("/")
    assert r.status_code == 200
    assert b'name="password"' in r.data

def test_bad_password_stays_on_home(client):
    r = client.post("/login", data={"password": "password"})
    assert b'name="password"' in r.data

def test_good_password_shows_welcome(client):
    r = client.post("/login", data={"password": "my-unique-passphrase-99"})
    assert b"Welcome" in r.data
    assert b"Logout" in r.data