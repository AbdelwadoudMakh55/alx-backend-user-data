#!/usr/bin/env python3
""" Module for authentication """


from api.v1.auth.auth import Auth
import base64
from models.user import User
from typing import TypeVar


class BasicAuth(Auth):
    """ Class that manages Basic authentication """

    def extract_base64_authorization_header(self,
                                            authorization_header: str) -> str:
        """ Extract Base64 from auth header """
        if authorization_header is None or \
           type(authorization_header) != str or not \
           authorization_header.startswith("Basic "):
            return None
        return authorization_header[6:]

    def decode_base64_authorization_header(
        self,
        base64_authorization_header: str
    ) -> str:
        """ Decode base64 from auth header """
        if base64_authorization_header is None or \
           type(base64_authorization_header) != str:
            return None
        try:
            decoded_str = base64.b64decode(base64_authorization_header)
            return decoded_str.decode('utf-8')
        except Exception:
            return None

    def extract_user_credentials(
        self,
        decoded_base64_authorization_header: str
    ) -> (str, str):
        """ Extract the user's credentials """
        if decoded_base64_authorization_header is None or \
           type(decoded_base64_authorization_header) != str or \
           ":" not in decoded_base64_authorization_header:
            return None, None
        idx = decoded_base64_authorization_header.index(":")
        email = decoded_base64_authorization_header[:idx]
        password = decoded_base64_authorization_header[idx + 1:]
        return email, password

    def user_object_from_credentials(self,
                                     user_email: str,
                                     user_pwd: str) -> TypeVar('User'):
        """ Return the user instance based on email and password """
        if user_email is None or type(user_email) != str:
            return None
        if user_pwd is None or type(user_pwd) != str:
            return None
        search = User.search({"email": user_email})
        if len(search) == 0:
            return None
        for user in search:
            if user.is_valid_password(user_pwd):
                return user

    def current_user(self, request=None) -> TypeVar('User'):
        """ Retrieve the current user """
        auth_header = self.authorization_header(request)
        if auth_header is not None:
            ext_auth = self.extract_base64_authorization_header(auth_header)
        else:
            return None
        decoded_header = self.decode_base64_authorization_header(ext_auth)
        if decoded_header is not None:
            email, password = self.extract_user_credentials(decoded_header)
        else:
            return None
        user = self.user_object_from_credentials(email, password)
        return user
