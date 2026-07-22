import os
from flask import Flask, request, render_template_string

app = Flask(__name__)

_LIST = os.path.join(os.path.dirname(__file__), "10-million-password-list-top-1000.txt")
with open(_LIST, encoding="utf-8") as f:
    COMMON_PASSWORDS = {line.strip() for line in f if line.strip()}

def verify_password(password: str) -> bool:
    if password is None:
        return False
    if not 8 <= len(password) <= 128:
        return False
    if password in COMMON_PASSWORDS:
        return False
    return True

HOME = """<form method="post" action="/login">
  <input type="password" name="password" placeholder="Password">
  <button type="submit">Login</button>
</form>"""

WELCOME = """<p>Welcome! Your password: {{ password }}</p>
<form method="get" action="/"><button type="submit">Logout</button></form>"""


@app.route("/")
def home():
    return render_template_string(HOME)


@app.route("/login", methods=["POST"])
def login():
    password = request.form.get("password", "")
    if verify_password(password):
        return render_template_string(WELCOME, password=password)
    return render_template_string(HOME)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)