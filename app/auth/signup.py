from flask import request, jsonify
from models import User, db, bcrypt

@main.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Validate input
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    # Check if user already exists
    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "User already exists"}), 400

    # Hash the password
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')

    # Create new user
    new_user = User(
        full_name=data.get('full_name', ''),
        email=data['email'],
        password=hashed_password
    )

    # Save user to database
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User created successfully"}), 201