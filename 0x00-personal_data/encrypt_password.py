#!/usr/bin/env python3
"""
Encrypt a password
"""


import bcrypt


def hash_password(password -> str) -> bytes:
    """ Function that hashes a password """
    password = password.encode()
    return bcrypt.hashpw(password, bcrypt.gensalt())
