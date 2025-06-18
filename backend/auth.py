import os
import json
from dotenv import load_dotenv
from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from werkzeug.security import check_password_hash
from uuid import uuid4
from redis import Redis
from model.models import db, User, Admin
from sqlalchemy.exc import IntegrityError
from flask_jwt_extended import JWTManager, create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

load_dotenv()

auth_user = Blueprint("auth_user", __name__)
redis_conn = Redis.from_url(os.getenv("REDIS_URL"))

# ---------------------- JWT setup & Blacklist check ---------------------------
@auth_user.record_once
def set_jwt_callbacks(state):
    jwt = JWTManager(state.app)

    @jwt.token_in_blocklist_loader
    def is_token_blacklisted(jwt_header, jwt_payload):
        return redis_conn.get(jwt_payload["jti"]) is not None
    
    @jwt.unauthorized_loader
    def custom_unauthorized(callback):
        return jsonify({"msg": "Missing or Invalid token"}), 401

# ------------------------- Role required decorators ----------------------------------

def role_required(required_role):
    def wrapper(func):
        @jwt_required()
        def decorator(*args, **kwargs):
            claims = get_jwt()
            if claims.get("role") != required_role:
                return jsonify({"msg": "Access Unauthorized"}), 403
            return func(*args, **kwargs)
        decorator.__name__ = func.__name__
        return decorator
    return wrapper

# --------------------------- Routes ---------------------------------------------

# Login route
@auth_user.post("/login/")
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = "user"

    user = User.query.filter_by(email=email).first()
    if not user:
        user = Admin.query.filter_by(email=email).first()
        role = "admin"
    
    success = user and check_password_hash(user.password, password)
    
    user_id = user.admin_id if role == "admin" else (user.user_id if user else "unknown")

    # save Login history in Redis
    login_data = {
        "user_id": user_id,
        "username": user.username if role == "user" and user else "unknown",
        "role_type": role,
        "ip_address": request.remote_addr,
        "agent": request.headers.get("User-Agent"),
        "success": success,
        "login_time": datetime.now().strftime("%H:%M:%S")
    }
    redis_conn.rpush("login_details", json.dumps(login_data))
    
    # history = LoginHistory(
    #     user_id = user_id,
    #     role_type = role,
    #     ip_address = request.remote_addr,
    #     user_agent = request.headers.get("user_agent"),
    #     success = success,
    #     login_time = datetime.now().strftime("%H:%M:%S")
    # )
    # db.session.add(history)
    # db.session.commit()

    if not success:
        return jsonify({
            "msg": "Invalid Credentials",
            "redirect": "/register/",  # vue can catch it and redirects
        }), 401
    
    # Successful login & create tokens
    access_token = create_access_token(
        identity=user_id,
        additional_claims={"role": role},
        expires_delta=timedelta(minutes=45)
    )
    refresh_token = create_refresh_token(
        identity=user_id,
        additional_claims={"role": role},
        expires_delta=timedelta(days=7)
    )

    return jsonify({
        "access_token": access_token,
        "refresh_token": refresh_token,
        "role": role
    }), 200

# Register route
@auth_user.post("/register/")
def register():
    data = request.get_json()
    if User.query.filter_by(email=data["email"]).first():
        return jsonify({
            "msg": "Email already exists",
            "redirect": "/login/"
        }), 409
    try:
        dob = data.get("dob")
        dob_obj = datetime.strptime(dob, "%Y-%m-%d").date()
        new_user = User(
            user_id = str(uuid4()),
            username = data["username"],
            email = data["email"],
            full_name = data["full_name"],
            qualification = data.get("qualification"),
            dob = dob_obj,
            location = data.get("location"),
            role_type = "user",
        )
        new_user.set_password(data["password"])
        db.session.add(new_user)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        return jsonify({"msg": "User has already exists"}), 409
    
    return jsonify({"msg": "User has registered successfully"}), 201

# refresh token route
@auth_user.post("/refresh/")
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    claims = get_jwt()
    role = claims.get("role")

    new_access_token = create_access_token(
        identity=identity,
        additional_claims={"role": role},
        expires_delta=timedelta(minutes=45),
    )
    return jsonify({"access_token": new_access_token}), 200

# logout route
@auth_user.post("/logout/")
@jwt_required()
def logout():
    jti = get_jwt()["jti"]
    exp = get_jwt()["exp"]
    ttl = exp - int(datetime.now().timestamp())
    redis_conn.setex(jti, ttl, "revoked")

    # save logout history in Redis
    logout_data = {
        "user_id": get_jwt_identity(),
        "logout_time": datetime.now().strftime("%H:%M:%S")
    }
    redis_conn.rpush("logout_details", json.dumps(logout_data))
    
    return jsonify({"msg": "Logged out"}), 200
