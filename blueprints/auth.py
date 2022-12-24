from flask import Blueprint, render_template, url_for, redirect, flash
from sqlalchemy.exc import IntegrityError
from forms import SignUpForm, LoginForm
from models import db, User
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    """Handle user sign up and """
    form = SignUpForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                email=form.email.data,
                name=form.name.data,
                password=form.password.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Email already taken", 'danger')
            return render_template('auth/signup.html', form=form)

        login_user(user)
        return redirect(url_for('main.index'))

    else:
        return render_template('auth/signup.html', form=form)


@auth.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login and redirect to homepage on success."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(
            form.email.data,
            form.password.data
        )

        if user:
            flash(f"Hello, {user.name}!", "success")

            login_user(user)
            return redirect(url_for('main.index'))

        flash("Invalid credentials.", 'danger')

    return render_template('auth/login.html', form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))