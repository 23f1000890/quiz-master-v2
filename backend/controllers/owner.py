from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from auth import role_required

auth_admin = Blueprint("auth_admin", __name__)

@auth_admin.get("/")
@jwt_required()
@role_required("admin")
def admin_dashboard():
    return jsonify({"msg": "hello admin"})