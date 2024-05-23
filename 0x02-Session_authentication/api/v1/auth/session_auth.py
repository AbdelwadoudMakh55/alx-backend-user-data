#!/usr/bin/env python3
"""
SessionAuth class, inherits from Auth
"""

from api.v1.auth.auth import Auth
from models.user import User
import uuid
import sys


class SessionAuth(Auth):
    """
    Body of SessionAuth class
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """ Create the session """
        if user_id is None or type(user_id) != str:
            return None
        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """ Return user_id based on session id """
        if session_id is None or type(session_id) != str:
            return None
        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """ Return the current user based on cookie value """
        cookie_session_id = self.session_cookie(request)
        user_id = self.user_id_for_session_id(cookie_session_id)
        return User.get(user_id)

    def destroy_session(self, request=None):
        """ Delete session """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        user_id = self.user_id_for_session_id(session_id)
        if user_id is None:
            return False
        del self.user_id_by_session_id[session_id]
        return True
