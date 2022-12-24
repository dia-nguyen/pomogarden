from flask import Blueprint, redirect, url_for, render_template, flash, g
from flask_login import login_required, current_user
from plants import plant_shop
from models import db, Seed, PlantPlot

main = Blueprint('main', __name__)

@main.route('/')
def index():
    if current_user.is_authenticated:
        if not current_user.available_plots:
            flash(f"You don't have any seeds, go buy some!")
        return render_template('garden.html')
    return redirect(url_for('auth.login'))
