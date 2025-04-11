from flask import Flask, jsonify
from flask_cors import CORS
from app.ai_recommendations import ai_recommendations
from app.routes.mpesa_payment import mpesa_router

app = Flask(__name__)

# Configure CORS
CORS(app, resources={
    r"/api/*": {
        "origins": [
            "https://nairobi-nest.vercel.app/",  # Your hosted frontend
            "http://localhost:5173"           # Local development
        ],
        "methods": ["GET", "POST", "OPTIONS", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# Add health check endpoint
@app.route('/')
def health_check():
    return jsonify({"status": "healthy", "message": "Nairobi Nest Backend"})

# Register blueprints
app.register_blueprint(ai_recommendations, url_prefix="/api")
app.register_blueprint(mpesa_router, url_prefix="/api")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)