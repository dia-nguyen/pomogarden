from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from forms import SignUpForm, LoginForm
from models import db, User
from flask_login import login_user, logout_user, current_user
from flask_jwt_extended import (
    create_access_token,
    get_current_user,
    jwt_required,
)

auth = Blueprint('auth', __name__)


@auth.post('/signup')
def signup():
    """Handle user sign up and """
    data = request.get_json()
    form = SignUpForm(data=data)

    if form.validate_on_submit():
        try:
            user = User.signup(
                email=form.data["email"],
                name=form.data["name"],
                password=form.data["password"],
            )
            db.session.commit()
            access_token = create_access_token(identity=user.id)
            return jsonify(token=access_token), 201

        except IntegrityError:
            return (jsonify(status="error", message="Email already taken")), 409

    else:
        return (jsonify(status="error", message="Invalid credentials")), 500


@auth.post('/login')
def login():
    """Handle user login and redirect to homepage on success."""
    data = request.get_json()
    form = LoginForm(data=data)

    if form.validate_on_submit():
        user = User.authenticate(
            form.email.data,
            form.password.data
        )

        if user:
            access_token = create_access_token(identity=user.id)
            return jsonify(token=access_token), 201
        else:
            return (jsonify(status="error", message="Invalid credentials"))
    else:
        return jsonify(errors=form.errors), 400


@auth.get('/users/<int:id>')
@jwt_required()
def user_profile(id):
    """Gets all user information associated with user id"""
    try:
        user = User.query.get_or_404(id)
        return jsonify(user=user.serialize())
    except Exception as e:
        return jsonify(errors=e), 404
