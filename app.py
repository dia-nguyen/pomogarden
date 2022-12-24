import os
from dotenv import load_dotenv

from flask import Flask, render_template, redirect, url_for, flash, g
from flask_sqlalchemy import SQLAlchemy
from blueprints.auth import auth as auth_blueprint
from blueprints.main import main as main_blueprint
from blueprints.garden import garden as garden_blueprint
from models import db, User, PlantPlot, Seed, connect_db
from flask_login import LoginManager, current_user
from plants import plant_shop

app = Flask(__name__)
load_dotenv()

#config
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ['DATABASE_URL'].replace("postgres://", "postgresql://"))
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ['SECRET_KEY']

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

connect_db(app)
db.create_all()

#register blueprints
app.register_blueprint(auth_blueprint)
app.register_blueprint(main_blueprint)
app.register_blueprint(garden_blueprint)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def add_available_plots():
    """Adds ids of liked messages to flask global."""
    if current_user.is_authenticated:
        current_user.available_plots = {plant_plot for plant_plot in current_user.plant_plots if plant_plot.status != "sold"}

@app.before_request
def add_shop_to_global():
    """Adds shop items available globally"""
    g.seeds = plant_shop()
