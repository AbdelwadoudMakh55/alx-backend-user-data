#!/usr/bin/env python3
""" Module for SessionDBAuth Class """


from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta


class SessionDBAuth(SessionExpAuth):
    """ SessionDBAuth inherits from SessionExpAuth """

    def create_session(self, user_id=None):
        """ Create session_id """
        session_id = super().create_session(user_id)
        user_session = UserSession({
            "user_id": user_id,
            "session_id": session_id,
            "created_at": datetime.now()
        })
        user_session.save()
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """ Retrieve user_id for session_id """
        duration = self.session_duration
        if session_id is None:
            return None
        users = UserSession.search({"session_id": session_id})
        if len(users) == 0:
            return None
        if duration <= 0:
            return users[0].user_id
        cr_at = users[0].created_at
        if cr_at + timedelta(seconds=duration) < datetime.now():
            return None
        user_id = users[0].user_id
        return user_id

    def destroy_session(self, request=None):
        """ Destroy session based on request """
        if request is None:
            return None
        session_id = self.session_cookie(request)
        if session_id is None:
            return False
        users = UserSession.search({"session_id": session_id})
        if len(users) == 0:
            return None
        user_id = users[0].user_id
        if user_id is None:
            return False
        users[0].remove()
        return True
