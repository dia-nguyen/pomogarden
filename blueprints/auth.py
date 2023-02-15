from flask import Blueprint, jsonify, request
from sqlalchemy.exc import IntegrityError
from forms import SignUpForm, LoginForm
from models import db, User
from flask_login import login_user, logout_user, current_user

auth = Blueprint('auth', __name__)


@auth.post('/signup')
def signup():
    """Handle user sign up and """
    if current_user.is_authenticated:
        return (jsonify(status="error", message="You are currently logged in"))

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

        except IntegrityError:
            return (jsonify(status="error", message="Email already taken"))

        login_user(user, remember=True)
        return (jsonify(status="success", name=f"{current_user.name}", email=f"{current_user.email}", message=f"Welcome {current_user.name}"), 201)

    else:
        return (jsonify(status="error", message="Invalid credentials"))


@auth.post('/login')
def login():
    """Handle user login and redirect to homepage on success."""
    if current_user.is_authenticated:
        return (jsonify(status="error", message="You are currently logged in"))

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.email.data,
            form.password.data
        )

        if user:
            login_user(user, remember=True)
            return (jsonify(status="success", name=f"{current_user.name}", email=f"{current_user.email}", message=f"Welcome back {current_user.name}"), 201)


    return (jsonify(status="error", message="Invalid credentials"))


@auth.post('/logout')
def logout():
    if current_user.is_authenticated:
        logout_user()
        return jsonify(status="success", message="You've successfully logged out.")
    return (jsonify(status="error", message="You are currently not logged in"))


