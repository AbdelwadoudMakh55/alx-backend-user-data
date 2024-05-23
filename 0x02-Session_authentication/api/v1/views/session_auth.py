#!/usr/bin/env python3
"""
Views for Session
"""

from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login():
    """ Handle session authentication """
    email = request.form.get('email')
    password = request.form.get('password')
    if email is None or email == '':
        return jsonify({'error': "email missing"}), 400
    if password is None or password == '':
        return jsonify({'error': "password missing"}), 400
    users = User.search({"email": email})
    if len(users) == 0:
        return jsonify({'error': "no user found for this email"}), 404
    user = None
    for user_ in users:
        if user_.is_valid_password(password):
            user = user_
    if user is None:
        return jsonify({'error': "wrong password"}), 401
    from api.v1.app import auth
    session_id = auth.create_session(user.id)
    response = jsonify(user.to_json())
    cookie_session_id = os.getenv("SESSION_NAME")
    response.set_cookie(cookie_session_id, session_id)
    return response
