import requests
from requests.auth import HTTPBasicAuth
import base64
from datetime import datetime
from django.conf import settings

# Get OAuth Token
def get_mpesa_token():
    url = "https://api.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(url, auth=HTTPBasicAuth(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    response.raise_for_status()
    return response.json().get("access_token")

# Initiate STK Push
def lipa_na_mpesa(phone_number, amount, account_reference, transaction_desc):
    token = get_mpesa_token()
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password_str = settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp
    password = base64.b64encode(password_str.encode()).decode()

    stk_url = "https://api.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {token}"}

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": amount,
        "PartyA": phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": account_reference,
        "TransactionDesc": transaction_desc
    }

    response = requests.post(stk_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()
# Check Transaction Status
def check_transaction_status(checkout_request_id):
    token = get_mpesa_token()
    status_url = "https://api.safaricom.co.ke/mpesa/stkpushquery/v1/query"
    headers = {"Authorization": f"Bearer {token}"}

    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    password_str = settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + timestamp
    password = base64.b64encode(password_str.encode()).decode()

    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": password,
        "Timestamp": timestamp,
        "CheckoutRequestID": checkout_request_id
    }

    response = requests.post(status_url, json=payload, headers=headers)
    response.raise_for_status()
    return response.json()  