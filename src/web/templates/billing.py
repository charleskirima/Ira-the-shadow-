import requests
import base64
import datetime

# These should be defined securely in your environment or config
BUSINESS_SHORTCODE = "123456"  # Replace with your Paybill or Till number
PASSKEY = "your_lnp_passkey_here"  # From M-Pesa developer portal
CALLBACK_URL = "https://yourdomain.com/api/payment/callback"
STK_PUSH_URL = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"

def get_mpesa_token():
    """
    Implement token generation by making a request to:
    https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials
    Use Basic Auth with your consumer key and secret.
    """
    consumer_key = "your_consumer_key"
    consumer_secret = "your_consumer_secret"

    auth = base64.b64encode(f"{consumer_key}:{consumer_secret}".encode()).decode()
    headers = {
        "Authorization": f"Basic {auth}"
    }

    res = requests.get(
        "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials",
        headers=headers
    )
    res.raise_for_status()
    return res.json()["access_token"]


def initiate_stk_push(phone_number, amount):
    timestamp = datetime.datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(
        f"{BUSINESS_SHORTCODE}{PASSKEY}{timestamp}".encode()
    ).decode()

    access_token = get_mpesa_token()

    payload = {
        "BusinessShortCode": BUSINESS_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": BUSINESS_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": CALLBACK_URL,
        "AccountReference": "IRA Subscription",
        "TransactionDesc": "Monthly IRA Access"
    }

    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }

    res = requests.post(STK_PUSH_URL, json=payload, headers=headers)
    return res.json()