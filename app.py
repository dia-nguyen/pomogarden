import os
from dotenv import load_dotenv

from flask import Flask, render_template, redirect, url_for, flash, g
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from blueprints.auth import auth as auth_blueprint
from blueprints.main import main as main_blueprint
from blueprints.garden import garden as garden_blueprint
from blueprints.shop import shop as shop_blueprint
from models import db, User, PlantPlot, Seed, connect_db
from plants import plant_shop
from flask_jwt_extended import (
    get_jwt_identity,
    jwt_required,
    JWTManager
)

app = Flask(__name__)
load_dotenv()
jwt = JWTManager(app)

CORS(app)

#config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

app.config['WTF_CSRF_ENABLED'] = False

app.config["JWT_ACCESS_TOKEN_EXPIRES"] = False
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = False

connect_db(app)
db.create_all()

#register blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(garden_blueprint)
app.register_blueprint(shop_blueprint)

@app.before_request
@jwt_required(optional=True)
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""
    try:
        g.user = User.query.filter_by(id=get_jwt_identity()).one_or_none()
    except:
        g.user = None