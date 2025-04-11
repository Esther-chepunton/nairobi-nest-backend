# mpesa_payments.py

from flask import Blueprint, request, jsonify
import requests
import os
import base64
from datetime import datetime

mpesa_router = Blueprint('mpesa', __name__)  # ✅ Flask blueprint

# Credentials

MPESA_CONSUMER_KEY = os.getenv("xiwYMbb06a8J9xmWKR3ZvNVrXdnUeAZEeeiFpvxgcD80yxAc")
MPESA_CONSUMER_SECRET = os.getenv("GGizuKomNt94fwAZJctO3zr53SxGyuqe2E6qqxCiGG9eG2v77qsffvDLxH41MpFw")
MPESA_SHORTCODE = os.getenv("MPESA_SHORTCODE")
MPESA_PASSKEY = os.getenv("MPESA_PASSKEY")

# Token Generator
def get_mpesa_access_token():
    try:
        auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
        
        # Verify credentials exist
        if not MPESA_CONSUMER_KEY or not MPESA_CONSUMER_SECRET:
            raise Exception("M-Pesa credentials not configured")
            
        # Debug print (remove in production)
        print(f"Using Consumer Key: {MPESA_CONSUMER_KEY[:4]}...{MPESA_CONSUMER_KEY[-4:]}")
        
        response = requests.get(
            auth_url,
            auth=(MPESA_CONSUMER_KEY, MPESA_CONSUMER_SECRET),
            headers={'Cache-Control': 'no-cache'},
            timeout=30
        )
        
        # Debug the raw response
        print(f"Auth response status: {response.status_code}")
        print(f"Auth response body: {response.text}")
        
        if response.status_code == 400:
            raise Exception("Invalid credentials or bad request")
            
        response.raise_for_status()  # Will raise for 4XX/5XX status codes
        
        return response.json()['access_token']
        
    except Exception as e:
        raise Exception(f"Token generation failed: {str(e)}")
# Payment Route
@mpesa_router.route("/mpesa-payment", methods=["POST"])
def mpesa_payment():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No data provided"}), 400
        
    phone_number = data.get("phone_number")
    amount = data.get("amount")
    
    if not phone_number or not amount:
        return jsonify({
            "status": "error",
            "message": "Phone number and amount are required"
        }), 400
        
    # Validate Kenyan phone number format
    if not phone_number.startswith("254") or len(phone_number) != 12:
        return jsonify({
            "status": "error",
            "message": "Phone number must be in 2547XXXXXXXX format"
        }), 400
    
    try:
        data = request.get_json()
        phone_number = data.get("phone_number")
        amount = data.get("amount")

        token = get_mpesa_access_token()
        if not token:
            return jsonify({"status": "error", "message": "Failed to get token"}), 500

        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        password = base64.b64encode(f"{MPESA_SHORTCODE}{MPESA_PASSKEY}{timestamp}".encode()).decode()

        payment_payload = {
            "BusinessShortCode": MPESA_SHORTCODE,
            "Password": password,
            "Timestamp": timestamp,
            "TransactionType": "CustomerPayBillOnline",
            "Amount": amount,
            "PartyA": phone_number,
            "PartyB": MPESA_SHORTCODE,
            "PhoneNumber": phone_number,
            "CallBackURL": "https://yourbackend.com/mpesa-callback",
            "AccountReference": "HotelBooking",
            "TransactionDesc": "Hotel Payment"
        }

        headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
        mpesa_response = requests.post(
            "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest",
            json=payment_payload,
            headers=headers
        )

        if mpesa_response.status_code == 200:
            return jsonify({
                "status": "success",
                "message": "Payment initiated",
                "details": mpesa_response.json()
            }), 200
        else:
            return jsonify({
                "status": "error",
                "message": "Failed to initiate payment",
                "details": mpesa_response.json()
            }), 500

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
