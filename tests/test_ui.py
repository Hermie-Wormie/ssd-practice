import os

BASE_URL = os.environ.get("BASE_URL", "http://127.0.0.1")


def test_bad_password_stays_on_home(page):
    page.goto(BASE_URL)
    page.fill('input[name="password"]', "password")
    page.click("button")
    page.wait_for_selector('input[name="password"]')


def test_good_password_shows_welcome(page):
    page.goto(BASE_URL)
    page.fill('input[name="password"]', "my-unique-passphrase-99")
    page.click("button")
    page.wait_for_selector("text=Welcome")
    page.click("button")  # logout
    page.wait_for_selector('input[name="password"]')