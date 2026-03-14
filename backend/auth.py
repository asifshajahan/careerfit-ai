import json
import os
import hashlib
import re
from datetime import datetime
from typing import Optional, Dict

USERS_FILE = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'users.json')


def _load_users() -> Dict:
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, 'r') as f:
            return json.load(f)
    except Exception:
        return {}


def _save_users(users: Dict):
    os.makedirs(os.path.dirname(USERS_FILE), exist_ok=True)
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)


def _hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def _validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def signup_user(name: str, email: str, password: str) -> Dict:
    if not name or not email or not password:
        return {"success": False, "message": "All fields are required"}

    if not _validate_email(email):
        return {"success": False, "message": "Invalid email format"}

    if len(password) < 6:
        return {"success": False, "message": "Password must be at least 6 characters"}

    users = _load_users()
    email_lower = email.lower()

    if email_lower in users:
        return {"success": False, "message": "Email already registered"}

    users[email_lower] = {
        "name": name,
        "email": email_lower,
        "password": _hash_password(password),
        "created_at": datetime.now().isoformat(),
        "predictions": []
    }
    _save_users(users)

    return {
        "success": True,
        "message": "Account created successfully",
        "user": {"name": name, "email": email_lower}
    }


def login_user(email: str, password: str) -> Dict:
    if not email or not password:
        return {"success": False, "message": "Email and password are required"}

    users = _load_users()
    email_lower = email.lower()

    if email_lower not in users:
        return {"success": False, "message": "Invalid email or password"}

    user = users[email_lower]
    if user["password"] != _hash_password(password):
        return {"success": False, "message": "Invalid email or password"}

    return {
        "success": True,
        "message": "Login successful",
        "user": {"name": user["name"], "email": email_lower}
    }


def save_prediction(email: str, prediction: Dict):
    users = _load_users()
    email_lower = email.lower()
    if email_lower in users:
        if "predictions" not in users[email_lower]:
            users[email_lower]["predictions"] = []
        prediction["timestamp"] = datetime.now().isoformat()
        users[email_lower]["predictions"].append(prediction)
        _save_users(users)
