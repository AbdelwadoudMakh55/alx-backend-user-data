#!/usr/bin/env python3
""" Module for authentication """


from api.v1.auth.auth import Auth


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
