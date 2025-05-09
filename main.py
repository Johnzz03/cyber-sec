from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_migrate import Migrate
from website import create_app, db
from website.models import Contact  # Import the Contact model

app = create_app()
migrate = Migrate(app, db)

@app.before_request
def method_override():
    if request.method == 'POST' and '_method' in request.form:
        method = request.form['_method'].upper()
        if method in ['PUT', 'DELETE']:
            request.environ['REQUEST_METHOD'] = method

@app.route('/admin/contacts', methods=['GET'], endpoint='admin_contacts')
def get_contacts():
    contacts = Contact.query.all()
    for contact in contacts:
        print(f"Contact: {contact.name}, {contact.email}, {contact.message}, {contact.created_at}")
    return render_template('admin_contacts.html', contacts=contacts)

@app.route('/admin/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get_or_404(id)
    return jsonify(contact.to_dict())

@app.route('/admin/contacts', methods=['POST'])
def create_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    # Validate the form data
    if not name or not email or not message:
        return render_template('contact.html', error="All fields are required!")

    # Save the contact to the database
    new_contact = Contact(name=name, email=email, message=message)
    db.session.add(new_contact)
    db.session.commit()

    # Redirect back to the contact.html page with a success message
    return render_template('contact.html', success="Your message has been saved successfully!")

@app.route('/admin/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)  # Fetch the contact by ID or return 404
    data = request.json  # Get the JSON data from the request
    for key, value in data.items():
        setattr(contact, key, value)  # Update the contact's attributes
    db.session.commit()  # Save changes to the database
    return jsonify(contact.to_dict())  # Return the updated contact as JSON

@app.route('/admin/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)  # Fetch the contact by ID or return 404 if not found
    db.session.delete(contact)  # Delete the contact from the database
    db.session.commit()  # Commit the changes
    return redirect(url_for('admin_contacts'))  # Redirect back to the admin contacts page

@app.route('/admin/contacts/delete_all', methods=['POST'])
def delete_all_contacts():
    # Delete all contacts from the database
    Contact.query.delete()
    db.session.commit()
    return redirect(url_for('admin_contacts'))

@app.route('/admin/contacts/delete_one', methods=['POST'])
def delete_one_contact():
    # Fetch the first contact in the database
    contact = Contact.query.first()
    if contact:
        db.session.delete(contact)  # Delete the contact
        db.session.commit()  # Commit the changes
        return redirect(url_for('admin_contacts'))  # Redirect back to the admin contacts page
    else:
        return jsonify({"message": "No contacts to delete."}), 404

@app.route('/admin/contacts/ids', methods=['GET', 'POST'])
def get_all_contact_ids():
    if request.method == 'POST':
        # Handle POST request logic here
        return jsonify({"message": "POST method is not implemented yet."})
    # Default behavior for GET
    contact_ids = [contact.id for contact in Contact.query.all()]
    return jsonify({"contact_ids": contact_ids})

@app.route('/admin/contacts/delete_by_name', methods=['POST'])
def delete_contact_by_name():
    name = request.form.get('name')  # Get the name from the form
    print(f"Name received: {name}")  # Debugging

    contact = Contact.query.filter_by(name=name).first()  # Find the contact by name
    if contact:
        print(f"Deleting contact: {contact.name}, {contact.email}")  # Debugging
        db.session.delete(contact)  # Delete the contact
        db.session.commit()  # Commit the changes
        return redirect(url_for('admin_contacts'))  # Redirect back to the admin contacts page
    else:
        print(f"No contact found with name '{name}'")  # Debugging
        return jsonify({"message": f"No contact found with name '{name}'."}), 404

@app.route('/admin/contacts/delete_by_id', methods=['POST'])
def delete_contact_by_id():
    contact_id = request.form.get('id')  # Get the ID from the form
    if contact_id:
        contact = Contact.query.get(contact_id)  # Find the contact by ID
        if contact:
            db.session.delete(contact)  # Delete the contact
            db.session.commit()  # Commit the changes
            return redirect(url_for('admin_contacts'))  # Redirect to the admin contacts page
        else:
            return jsonify({"message": f"No contact found with ID {contact_id}."}), 404
    else:
        return jsonify({"message": "Invalid ID provided."}), 400
@app.route('/admin/contacts/edit', methods=['GET', 'POST'])
def edit_contact():
    contact_id = request.args.get('id')  # Get the contact ID from the query string
    contact = Contact.query.get_or_404(contact_id)

    if request.method == 'POST':
        # Update the contact details
        contact.name = request.form.get('name')
        contact.email = request.form.get('email')
        contact.message = request.form.get('message')
        db.session.commit()
        return redirect(url_for('admin_contacts'))

    # Render the edit form
    return render_template('edit_contact.html', contact=contact)    

@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create the database and tables
        print("Database and tables created successfully!")

        contacts = Contact.query.all()
        for contact in contacts:
            print(f"Contact: {contact.name}, {contact.email}, {contact.message}")

    app.run(host='0.0.0.0', port=5000, debug=True)