#!/usr/bin/env python3
""" Module for authentication """


from api.v1.auth.auth import Auth
import base64


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
