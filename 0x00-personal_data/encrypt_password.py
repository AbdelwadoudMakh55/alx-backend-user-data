#!/usr/bin/env python3
"""
Encrypt a password using the bcrypt package
"""
import bcrypt


def hash_password(password: str) -> bytes:
    """ Function that hashes a password """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())


def is_valid(hashed_password: bytes, password: str) -> bool:
    """ Validate if a password is the same as the hash """
    return bcrypt.checkpw(hashed_password, hash_password(password))
