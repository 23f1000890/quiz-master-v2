from flask import Blueprint, jsonify
from flask_jwt_extended import jwt_required
from auth import role_required

reg_user = Blueprint("reg_user", __name__)

@reg_user.get("/")
@jwt_required()
@role_required("user")
def user_dashboard():
    return jsonify({"msg": "hello user"})