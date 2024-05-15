#!/usr/bin/env python3
"""
Encrypt a password using the bcrypt package
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Function that hashes a password """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())
