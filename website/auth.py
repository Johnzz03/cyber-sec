from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db, csrf

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        # Query the database for the user
        user = User.query.filter_by(username=username).first()

        if user:
            # Check if the password is correct
            if check_password_hash(user.password, password):
                flash('Login successful!', category='success')
                login_user(user)
                return redirect(url_for('views.homepage'))  # Redirect to homepage
            else:
                flash('Incorrect password, please try again.', category='error')
        else:
            flash('Username does not exist.', category='error')

    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', category='success')
    return redirect(url_for('views.homepage'))  # Redirect to the homepage

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        print(request.form)  # Debugging: Print the form data to the console

        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        # Check if the user already exists
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        else:
            # Use 'pbkdf2:sha256' as the hashing method
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()

            flash('Account created successfully!', category='success')
            return redirect(url_for('auth.login'))

    return render_template('signup.html')

views = Blueprint('views', __name__)

@views.route('/homepage')
def homepage():
    return render_template('homepage.html')