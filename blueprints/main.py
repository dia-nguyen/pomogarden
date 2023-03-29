from flask import Blueprint,render_template, flash, g
from flask_jwt_extended import (
    jwt_required,
)

main = Blueprint('main', __name__)

@main.route('/')
@jwt_required
def index():
    if not g.user.plant_plots:
        flash(f"You don't have any seeds, go buy some!")
    return render_template('garden.html')
