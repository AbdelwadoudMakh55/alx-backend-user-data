#!/usr/bin/env python3
"""
Module that handles authentication
"""

import bcrypt


def _hash_password(password: str) -> bytes:
    """Hash a password"""
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
