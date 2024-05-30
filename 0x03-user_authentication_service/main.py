#!/usr/bin/env python3
"""
End-to-end integration test
"""
import requests


def register_user(email: str, password: str) -> None:
    """Test /users route"""
    data = {"email": email, "password": password}
    r = requests.post("http://127.0.0.1:5000/users", data=data)
    assert r.json() == {"email": email, "message": "user created"}


def log_in_wrong_password(email: str, password: str) -> None:
    """Test sessions login with wrong password"""
    data = {"email": email, "password": password}
    r = requests.post("http://127.0.0.1:5000/sessions", data=data)
    assert r.status_code == 401


def log_in(email: str, password: str) -> str:
    """Test correct login"""
    data = {"email": email, "password": password}
    r = requests.post("http://127.0.0.1:5000/sessions", data=data)
    assert r.json() == {"email": email, "message": "logged in"}
    return r.cookies.get("session_id")


def profile_unlogged() -> None:
    """Test /profile endpoint"""
    fake_session_id = {"session_id": "fidikdlmsdj"}
    r = requests.get("http://127.0.0.1:5000/profile", cookies=fake_session_id)
    assert r.status_code == 403


def profile_logged(session_id: str) -> None:
    cookies = {"session_id": session_id}
    r = requests.get("http://127.0.0.1:5000/profile", cookies=cookies)
    assert r.json() == {"email": EMAIL}


def log_out(session_id: str) -> None:
    cookies = {"session_id": session_id}
    r = requests.delete("http://127.0.0.1:5000/sessions", cookies=cookies)
    assert r.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    data = {"email": email}
    r = requests.post("http://127.0.0.1:5000/reset_password", data=data)
    assert r.status_code == 200
    return r.json().get("reset_token")


def update_password(email: str, reset_token: str, new_password: str) -> None:
    data = {
        "email": email, "reset_token": reset_token,
        "new_password": new_password
    }
    r = requests.put("http://127.0.0.1:5000/reset_password", data=data)
    assert r.json() == {"email": email, "message": "Password updated"}


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"


if __name__ == "__main__":

    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
