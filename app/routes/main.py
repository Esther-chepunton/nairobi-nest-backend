from flask import Blueprint

# Create a Blueprint instance
main = Blueprint('main', __name__)

@main.route('/hotels', methods=['GET'])
def get_hotels():
    # your route logic
    pass

# Add other routes as needed