from flask import jsonify
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token
from database import users_collection
from datetime import timedelta
import uuid

bcrypt = Bcrypt()

# ----------------------------
# Register User
# ----------------------------
def register_user(data):
    name = data.get("name")
    email = data.get("email")
    password = data.get("password")

    if not name or not email or not password:
        return jsonify({"message": "All fields are required"}), 400

    if users_collection.find_one({"email": email}):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode("utf-8")

    users_collection.insert_one({
        "_id": str(uuid.uuid4()),
        "name": name,
        "email": email,
        "password": hashed_password
    })

    return jsonify({"message": "User registered successfully"}), 201


# ----------------------------
# Login User
# ----------------------------
def login_user(data):
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"message": "Email and password required"}), 400

    user = users_collection.find_one({"email": email})
    if not user:
        return jsonify({"message": "User not found"}), 404

    if not bcrypt.check_password_hash(user["password"], password):
        return jsonify({"message": "Invalid credentials"}), 401

    token = create_access_token(
        identity=user["_id"],
        expires_delta=timedelta(days=1)
    )

    return jsonify({
        "message": "Login successful",
        "token": token,
        "user_id": user["_id"],
        "name": user["name"]
    }), 200