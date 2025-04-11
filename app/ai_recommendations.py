from flask import Blueprint, request, jsonify
import json
import os
from geopy.distance import geodesic

ai_recommendations = Blueprint('ai_recommendations', __name__)

# Load hotel data (replace with a database call if needed)
json_path = os.path.join(os.path.dirname(__file__), "hotel.json")
with open(json_path, "r") as file:
    hotel_data = json.load(file)["hotels"]

@ai_recommendations.route("/recommendations", methods=["POST"])
def get_recommendations():
    try:
        data = request.json
        selected_lat = data["latitude"]
        selected_lng = data["longitude"]

        def calculate_distance(hotel):
            return geodesic((selected_lat, selected_lng), (hotel["latitude"], hotel["longitude"])).km

        # Sort hotels by distance and return top 5
        recommended_hotels = sorted(hotel_data, key=calculate_distance)[:5]
        for hotel in recommended_hotels:
            hotel["distance"] = calculate_distance(hotel)

        return jsonify({"status":"success", "data":recommended_hotels}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
