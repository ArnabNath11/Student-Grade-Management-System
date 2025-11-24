# test_check.py
from werkzeug.security import check_password_hash
import json, os, getpass

uf = 'users.json'
if not os.path.exists(uf):
    print("users.json not found")
    raise SystemExit

users = json.load(open(uf))

print("Users found:")
for i, u in enumerate(users, 1):
    print(f"{i}. username: {u.get('username')}, stored hash prefix: {u.get('password','')[:12]}")

username = input("Enter username to test: ").strip()
pw = getpass.getpass("Enter password to test: ")

user = next((u for u in users if u['username'] == username), None)
if not user:
    print("No such user (check case-sensitivity).")
else:
    ok = check_password_hash(user['password'], pw)
    print("check_password_hash returned:", ok)
    if not ok:
        print("Werkzeug cannot verify this stored hash with the password you entered.")
