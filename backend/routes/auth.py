from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from database import get_database
import jwt
import os
from datetime import datetime, timedelta

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        db = get_database()
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        users = db['users']
        data = request.json
        
        # Check if user already exists
        if users.find_one({'email': data['email']}):
            return jsonify({'error': 'User already exists'}), 400
        
        # Hash password
        hashed_password = generate_password_hash(data['password'])
        
        # Create user document
        user = {
            'email': data['email'],
            'username': data.get('username', data['email'].split('@')[0]),
            'password': hashed_password,
            'created_at': datetime.utcnow()
        }
        
        # Insert user
        result = users.insert_one(user)
        
        return jsonify({
            'message': 'User registered successfully',
            'user_id': str(result.inserted_id)
        }), 201
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        db = get_database()
        if db is None:
            return jsonify({'error': 'Database connection failed'}), 500
        
        users = db['users']
        data = request.json
        
        # Find user
        user = users.find_one({'email': data['email']})
        
        if not user or not check_password_hash(user['password'], data['password']):
            return jsonify({'error': 'Invalid credentials'}), 401
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': str(user['_id']),
            'email': user['email'],
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, os.getenv('JWT_SECRET_KEY'), algorithm='HS256')
        
        return jsonify({
            'message': 'Login successful',
            'token': token,
            'user': {
                'id': str(user['_id']),
                'email': user['email'],
                'username': user['username']
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500