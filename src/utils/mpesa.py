import base64
import datetime
import requests
import os

# ✅ Load these from environment or config
MPESA_ENV = os.getenv("MPESA_ENV", "sandbox")  # "production" or "sandbox"
BUSINESS_SHORTCODE = os.getenv("MPESA_SHORTCODE", "174379")  # Demo shortcode
PASSKEY = os.getenv("MPESA_PASSKEY")  # Get from Daraja
CONSUMER_KEY = os.getenv("MPESA_CONSUMER_KEY")
CONSUMER_SECRET = os.getenv("MPESA_CONSUMER_SECRET")
CALLBACK_URL = os.getenv("MPESA_CALLBACK_URL", "https://yourdomain.com/billing/confirm")

# 🌍 API URLs
TOKEN_URL = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
STK_PUSH_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

def get_mpesa_token():
    response = requests.get(
        TOKEN_URL,
        auth=(CONSUMER_KEY, CONSUMER_SECRET)
    )
    if response.status_code == 200:
        return response.json()["access_token"]
    raise Exception(f"Failed to obtain M-Pesa token: {response.text}")

def send_stk_push(phone_number: str, amount: int = 1500):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    data_to_encode = f"{BUSINESS_SHORTCODE}{PASSKEY}{timestamp}"
    encoded_password = base64.b64encode(data_to_encode.encode()).decode()

    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": encoded_password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "IRA-Sub",
        "TransactionDesc": "IRA Monthly Subscription"
    }

    headers = {
        "Authorization": f"Bearer {get_mpesa_token()}",
        "Content-Type": "application/json"
    }

    response = requests.post(STK_PUSH_URL, json=payload, headers=headers)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"STK Push Failed: {response.text}")