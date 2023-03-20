"""SQLAlchemy models for CAPSTONE."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()




class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(
        db.Integer,
        primary_key=True,
    )

    email = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    username = db.Column(
        db.Text,
        nullable=False,
        unique=True,
    )

    image_url = db.Column(
        db.Text,
        default="/static/images/default-pic.png",
    )

    header_image_url = db.Column(
        db.Text,
        default=None,
    )

    bio = db.Column(
        db.Text,
    )

    
    password = db.Column(
        db.Text,
        nullable=False,
    )

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"

   
    @classmethod
    def signup(cls, username, email, password, image_url):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(
            username=username,
            email=email,
            password=hashed_pwd,
            image_url=image_url,
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False




class Fridge(db.Model):
    """Fridge"""

    __tablename__='fridges'


    id=db.Column(db.Integer,primary_key=True)
    
    ingredients=db.Column(db.Text,unique=True)

    grocerylist=db.Column(db.Text,unique=True)

    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),unique=True)



class Meals(db.Model):
    """meals and recipes for user"""
    __tablename__='meals'

    id=db.Column(db.Integer,primary_key=True)
    recipes=db.Column(db.Text,unique=True,nullable=True)
    mealplans=db.Column(db.Text,nullable=True)
    fridge_id=db.Column(db.Integer,db.ForeignKey('fridges.id'),unique=True,nullable=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'),unique=True)



def connect_db(app):
    """Connect this database to provided Flask app.

    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
#