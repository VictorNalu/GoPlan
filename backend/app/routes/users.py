#!/usr/bin/env python3
"""
This module defines the CRUD routes for the User model in GoPlan.
It includes routes for registering, logging in, retrieving, updating,
and deleting users.
"""

from flask import jsonify, request, abort
from app.models.user import User
from app import db
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.routes import app_views
from sqlalchemy.exc import IntegrityError

# REGISTER USER
@app_views.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """Register a new user"""
    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()
    required_fields = ['email', 'password', 'username', 'first_name', 'last_name']
    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        abort(400, description=f"Missing field(s): {', '.join(missing_fields)}")

    try:
        new_user = User()
        for key, value in data.items():
            if key not in ['id', 'created_at', 'updated_at', '__class__']:
                setattr(new_user, key, value)

        new_user.set_password(data['password'])
        new_user.validate_email()
        new_user.save()

        access_token = create_access_token(identity=new_user.id)
        return jsonify({
            "success": True,
            "access_token": access_token,
            "user": new_user.to_dict()
        }), 201

    except IntegrityError as e:
        db.session.rollback()
        if 'Duplicate entry' in str(e.orig):
            return jsonify({"error": "User with this email or username already exists"}), 409
        abort(500, description="An error occurred while registering the user.")
        
    except Exception as e:
        print(f"Error during user registration: {e}")
        abort(500, description="An error occurred while registering the user.")

# LOGIN USER
@app_views.route('/login', methods=['POST'], strict_slashes=False)
def login_user():
    """Log in a user"""
    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()
    user = User.query.filter(
        (User.email == data.get('email')) |
        (User.username == data.get('username'))
    ).first()

    if user and user.check_password(data.get('password')):
        access_token = create_access_token(identity=user.id)
        return jsonify({
            "success": True,
            "access_token": access_token,
            "user": user.to_dict()
        }), 200

    abort(401, description="Invalid credentials")

# GET A SINGLE USER
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_user(user_id):
    """Retrieve a user by ID"""
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")

    return jsonify(user.to_dict()), 200

# GET ALL USERS
@app_views.route('/users', methods=['GET'], strict_slashes=False)
@jwt_required()
def get_users():
    """Retrieve all users"""
    users = User.query.all()
    return jsonify([user.to_dict() for user in users]), 200

# UPDATE USER
@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
@jwt_required()
def update_user(user_id):
    """Update user details"""
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")

    if not request.is_json:
        abort(400, description="Request must be JSON")

    data = request.get_json()
    print("Received data for update:", data)

    try:
        ignore_keys = ["id", "created_at", "updated_at", "__class__"]

        for key, value in data.items():
            if key not in ignore_keys:
                if key == "password":
                    user.set_password(value)
                else:
                    setattr(user, key, value)

        db.session.commit()
        print("User updated successfully:", user.to_dict())

        return jsonify(user.to_dict()), 200

    except Exception as e:
        print(f"Error during user update: {e}")
        abort(500, description="An error occurred while updating the user.")

# DELETE USER
@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
@jwt_required()
def delete_user(user_id):
    """Delete a user by ID"""
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")

    try:
        user.delete()
        db.session.commit()
        return jsonify({"success": True, "message": "User deleted"}), 200

    except Exception as e:
        print(f"Error during user deletion: {e}")
        abort(500, description="An error occurred while deleting the user.")
