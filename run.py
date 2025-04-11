from flask import Flask
from flask_cors import CORS

from app.ai_recommendations import ai_recommendations  # adjust to your actual blueprint import
from app.routes.mpesa_payment import mpesa_router


app = Flask(__name__)

# ✅ Enable CORS for all routes
CORS(app)

# or be more strict with just localhost:5173:
# CORS(app, origins=["http://localhost:5173"])

# ✅ Register your blueprints
app.register_blueprint(ai_recommendations, url_prefix="/api")
app.register_blueprint(mpesa_router, url_prefix="/api")

if __name__ == "__main__":
    app.run(debug=True)
