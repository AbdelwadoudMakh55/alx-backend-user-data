#!/usr/bin/env python3
""" Module for authentication """


from flask import request
from typing import List, TypeVar

class Auth:
    """ Class that manages authenticatio """


    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ return false for now"""
        if path is None or excluded_paths is None or len(excluded_paths) == 0:
            return True
        elif path in excluded_paths:
            return False
        elif path[-1] == '/':
            if path[:-1] in excluded_paths:
                return False
        elif path[-1] != '/':
            if path + '/' in excluded_paths:
                return False
        return True

    def authorization_header(self, request=None) -> str:
        """ returns None for now"""
        if request is None or "Authorization" not in request.args.keys():
            return None
        return request.args.get("Authorization")

    def current_user(self, request=None) -> TypeVar('User'):
        """ returns None for now"""
        return None
