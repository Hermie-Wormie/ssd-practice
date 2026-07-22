import os
from flask import Flask, request, render_template_string
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.secret_key = os.environ["FLASK_SECRET"]
csrf = CSRFProtect(app)

_LIST = os.path.join(os.path.dirname(__file__), "10-million-password-list-top-1000.txt")
with open(_LIST, encoding="utf-8") as f:
    COMMON_PASSWORDS = {line.strip() for line in f if line.strip()}

HOME = """<form method="post" action="/login">
  <input type="hidden" name="csrf_token" value="{{ csrf_token() }}">
  <input type="password" name="password" placeholder="Password">
  <button type="submit">Login</button>
</form>"""

WELCOME = """<p>Welcome! Your password: {{ password }}</p>
<form method="get" action="/"><button type="submit">Logout</button></form>"""


def verify_password(password: str) -> bool:
    if password is None:
        return False
    if not 8 <= len(password) <= 128:
        return False
    if password in COMMON_PASSWORDS:
        return False
    return True


@app.route("/", methods=["GET"])
def home():
    return render_template_string(HOME)


@app.route("/login", methods=["POST"])
def login():
    password = request.form.get("password", "")
    if verify_password(password):
        return render_template_string(WELCOME, password=password)
    return render_template_string(HOME)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)