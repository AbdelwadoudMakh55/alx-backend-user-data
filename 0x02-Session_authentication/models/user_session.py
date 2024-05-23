#!/usr/bin/env python3
""" UserSession Model
"""


from models.base import Base


class UserSession(Base):
    """ UserSession inherits from Base """

    def __init__(self, *args: list, **kwargs: dict):
        """ Initialize UserSession Object """
        super().__init__(*args, **kwargs)
        self.user_id = kwargs.get('user_id')
        self.session_id = kwargs.get('session_id')
        self.created_at = kwargs.get('created_at')
