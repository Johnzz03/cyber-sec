from flask_login import UserMixin
from . import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

class FreeQuote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    message = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=db.func.current_timestamp())

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)  # NOT NULL constraint
    email = db.Column(db.String(120), nullable=False)  # NOT NULL constraint
    message = db.Column(db.Text, nullable=False)  # NOT NULL constraint
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

# Define the user_loader function
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))