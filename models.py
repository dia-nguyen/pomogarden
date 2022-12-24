"""SQLAlchemy models for user"""

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from wtforms.validators import DataRequired, Email, Length
from flask_login import UserMixin

bcrypt = Bcrypt()
db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User in the system."""

    __tablename__ = 'users'

    plant_plots = db.relationship(
        'PlantPlot',
        secondary='gardens',
        backref='users'
    )

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String(100),
        nullable=False,
    )
    email = db.Column(
        db.String(100),
        nullable=False,
        unique=True,
    )
    password = db.Column(
        db.String(100),
        nullable=False,
    )

    coins = db.Column(
        db.Integer,
        default = 200
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.name}, {self.email}>"

    @classmethod
    def signup(cls, name, email, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            name=name,
            email=email,
            password=hashed_pwd,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, email, password):
        """Find user with `email` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If this can't find matching user (or if password is wrong), returns
        False.
        """

        user = cls.query.filter_by(email=email).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False

    def add_coins(self, coins):
        """Add coins to user"""
        self.coins += coins

    def buy_seed(self, seed):
        if self.coins >= seed.buy_price:
            self.coins -= seed.buy_price
            new_plant_plot = PlantPlot(
                name = seed.name,
                current_sprite = seed.seed_sprite
            )
            self.plant_plots.append(new_plant_plot)
        else:
            raise ValueError("Not enough points to purchase")

class PlantPlot(db.Model):
    """Model for Plant plot in system"""

    __tablename__ = "plant_plots"

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    name = db.Column(
        db.String(50),
        nullable=False,
    )

    current_sprite = db.Column(
        db.Text()
    )

    status = db.Column(
        db.Text(),
        default = "empty"
    )

    age = db.Column(
        db.Text(),
    )

    watered = db.Column(
        db.Boolean(),
        default = False
    )

    sowed = db.Column(
        db.Boolean(),
        default = False
    )

    planted = db.Column(
        db.Boolean(),
        default = False
    )

    harvested = db.Column(
        db.Boolean(),
        default = False
    )

    def sow_plot(self):
        """sow plot"""
        self.sowed = True
        self.status = "sowed"

    def plant_seed(self, seed):
        """plant seed in plot"""
        self.planted = True
        self.status = "planted"
        self.age = "sprout"
        self.current_sprite = seed.sprout_sprite

    def water_plant(self):
        """water plant"""
        self.watered = True
        self.status = "watered"

    def age_one_day(self, seed):
        self.watered = False
        self.status = "thirsty"

        if self.age == "sprout":
            self.age = "seedling"
            self.current_sprite = seed.seedling_sprite

        elif self.age == "seedling":
            self.age = "ripe"
            self.current_sprite = seed.ripe_sprite

    def harvest_and_sell_plant(self, seed):
        if self.age == "ripe":
            self.current_sprite = seed.plant_sprite
            self.users[0].add_coins(seed.sell_price)
            self.status = "sold"



class Garden(db.Model):
    __tablename__ = "gardens"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id")
    )
    plant_plot_id = db.Column(
        db.Integer,
        db.ForeignKey("plant_plots.id")
    )

class Seed(db.Model):
    __tablename__ = "seeds"

    name = db.Column(
        db.Text,
        primary_key=True,
        unique = True
    )

    seed_sprite = db.Column(
        db.Text()
    )
    sprout_sprite = db.Column(
        db.Text()
    )
    seedling_sprite = db.Column(
        db.Text()
    )
    budding_sprite = db.Column(
        db.Text()
    )
    ripe_sprite = db.Column(
        db.Text()
    )
    plant_sprite = db.Column(
        db.Text()
    )
    buy_price = db.Column(
        db.Integer
    )
    sell_price = db.Column(
        db.Integer
    )


def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    app.app_context().push()
    db.app = app
    db.init_app(app)