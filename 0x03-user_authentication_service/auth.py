#!/usr/bin/env python3
"""
Module that handles authentication
"""

import bcrypt
from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    """Hash a password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        """Register a new user"""
        check_user = None
        try:
            check_user = self._db.find_user_by(email=email)
        except Exception:
            pass
        finally:
            if check_user:
                raise ValueError(f"User {email} already exists")
            hashed_pwd = _hash_password(password)
            return self._db.add_user(email, hashed_pwd)
