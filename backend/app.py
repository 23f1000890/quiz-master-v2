#importing all dependencies to run the flask
import os
from flask import Flask
from flask import jsonify
from dotenv import load_dotenv
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from model.models import db, Admin
from auth import auth_user
from controllers.owner import auth_admin
from controllers.users import reg_user
from redis_config import cache
from model.models import *

load_dotenv() #load variables from .env files

app = Flask(__name__) #initialize the app
CORS(app, supports_credentials=True) #enables CORS for all routes

#confugurations and modifications for the app
app.config["CACHE_TYPE"] = "RedisCache"
app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY")
app.config["CACHE_REDIS_URL"] = os.environ.get("REDIS_URL")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("SQLALCHEMY_DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["CACHE_DEFAULT_TIMEOUT"] = 180  # default expiry in seconds (3 minutes)

jwt = JWTManager(app) #initialize json web token authentication
cache.init_app(app) # initialize cache

# database initializations
db.init_app(app)
with app.app_context():
    db.create_all()
    admin = Admin.query.filter_by(email="admin123@admin.com").first()
    if not admin:
        admin = Admin(email="admin123@admin.com", role_type="admin")
        admin.set_password("Admin123")
        db.session.add(admin)
        db.session.commit()

# registering blueprints
app.register_blueprint(auth_user, url_prefix="/auth") # auth blueprint
app.register_blueprint(auth_admin, url_prefix="/admin") # admin blueprint
app.register_blueprint(reg_user, url_prefix="/user") # user blueprint


@app.get("/")
def quiz_server():
    return jsonify({
        "msg": "Welcome To IntelliQuest 2.0",
        "desc": "This is the Exam Preparation site for multiple courses. Anyone can give a Mock Test here and evaluate themselves."
    })


#run app
if __name__ == "__main__":
    app.run(debug=True, port=4001)