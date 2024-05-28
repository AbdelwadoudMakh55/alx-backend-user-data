#!/usr/bin/env python3
"""
Module that handles authentication
"""

import bcrypt
from db import DB
from user import User
import uuid


def _hash_password(password: str) -> bytes:
    """Hash a password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a UUID"""
    return uuid.UUID


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

    def valid_login(self, email: str, password: str) -> bool:
        """Credentials validation"""
        try:
            user = self._db.find_user_by(email=email)
            if bcrypt.checkpw(password.encode(), user.hashed_password):
                return True
            return False
        except Exception:
            return False
