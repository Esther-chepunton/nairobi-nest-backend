from flask_jwt_extended import create_access_token

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    # Validate input
    if not data or not data.get('email') or not data.get('password'):
        return jsonify({"error": "Email and password are required"}), 400

    # Find user by email
    user = User.query.filter_by(email=data['email']).first()
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Verify password
    if not bcrypt.check_password_hash(user.password, data['password']):
        return jsonify({"error": "Invalid password"}), 401

    # Create JWT token
    access_token = create_access_token(identity=user.id)
    return jsonify({"access_token": access_token}), 200