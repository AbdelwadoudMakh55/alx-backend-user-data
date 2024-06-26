#!/usr/bin/env python3
"""
SessionExpAuth class for session expiry date
"""


from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """ Body of the class: SessionExpAuth """

    def __init__(self):
        """ Initialize the object """
        duration = 0
        if os.getenv("SESSION_DURATION") is not None and \
           os.getenv("SESSION_DURATION").isnumeric():
            duration = int(os.getenv("SESSION_DURATION"))
        self.session_duration = duration

    def create_session(self, user_id=None):
        """ Create session """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None
        self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
        }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Return user_id using session_id """
        duration = self.session_duration
        user_id_by_session_id = self.user_id_by_session_id
        if session_id is None:
            return None
        if user_id_by_session_id.get(session_id) is None:
            return None
        if duration <= 0:
            return user_id_by_session_id.get(session_id).get("user_id")
        if user_id_by_session_id.get(session_id).get("created_at") is None:
            return None
        cr_at = user_id_by_session_id.get(session_id).get("created_at")
        if cr_at + timedelta(seconds=duration) < datetime.now():
            return None
        user_id = user_id_by_session_id.get(session_id).get("user_id")
        return user_id
