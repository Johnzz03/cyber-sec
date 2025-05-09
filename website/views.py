from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import FreeQuote, Contact  # Ensure Contact is imported
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template('home.html')

@views.route('/about')
def about():
    return render_template("about.html")

@views.route('/homepage')
def homepage():
    return render_template("homepage.html")

@views.route('/services')
def services():
    return render_template("services.html")

@views.route('/free-quote', methods=['GET', 'POST'])
def free_quote():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        message = request.form.get('message')

        # Save the data to the database
        new_quote = FreeQuote(name=name, email=email, message=message)
        db.session.add(new_quote)
        db.session.commit()

        flash('Your request for a free quote has been submitted successfully!', category='success')
        return redirect(url_for('views.home'))  # Redirect to homepage or another page

    return render_template('free_quote.html')  # Render the free quote page for GET requests

@views.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        contact_message = request.form.get('contact')  # Use a different name
        message = request.form.get('message')

        flash('Your message has been sent successfully!', category='success')

    return render_template('contact.html')

@views.route('/admin/quotes')
@login_required
def admin_quotes():
    if not current_user.is_admin:  # Assuming `is_admin` is a field in your User model
        flash('You do not have permission to access this page.', category='error')
        return redirect(url_for('views.home'))

    quotes = FreeQuote.query.all()
    return render_template('admin_quotes.html', quotes=quotes)