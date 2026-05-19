import os
import base64
import json
import requests
from datetime import datetime
from models import db, User, Payment
from config import Config


def get_access_token():
    consumer_key = os.environ.get('MPESA_CONSUMER_KEY', '')
    consumer_secret = os.environ.get('MPESA_CONSUMER_SECRET', '')
    api_url = 'https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    if not consumer_key or not consumer_secret:
        return None

    try:
        resp = requests.get(api_url, auth=(consumer_key, consumer_secret), timeout=30)
        if resp.status_code == 200:
            return resp.json().get('access_token')
    except Exception as e:
        print(f"MPESA access token error: {e}")
    return None


def get_timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')


def get_password(shortcode, passkey, timestamp):
    return base64.b64encode(f'{shortcode}{passkey}{timestamp}'.encode()).decode()


def stk_push(phone_number, amount, account_reference, transaction_desc):
    token = get_access_token()
    if not token:
        return {'error': 'Failed to get access token'}

    shortcode = os.environ.get('MPESA_SHORTCODE', '174379')
    passkey = os.environ.get('MPESA_PASSKEY', '')
    callback_url = os.environ.get('MPESA_CALLBACK_URL', 'https://your-domain.com/payments/mpesa-callback')

    timestamp = get_timestamp()
    password = get_password(shortcode, passkey, timestamp)

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'BusinessShortCode': shortcode,
        'Password': password,
        'Timestamp': timestamp,
        'TransactionType': 'CustomerPayBillOnline',
        'Amount': amount,
        'PartyA': phone_number,
        'PartyB': shortcode,
        'PhoneNumber': phone_number,
        'CallBackURL': callback_url,
        'AccountReference': account_reference,
        'TransactionDesc': transaction_desc
    }

    try:
        resp = requests.post(
            'https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest',
            headers=headers,
            json=payload,
            timeout=30
        )
        return resp.json()
    except Exception as e:
        return {'error': str(e)}


def query_status(checkout_request_id):
    token = get_access_token()
    if not token:
        return {'error': 'Failed to get access token'}

    shortcode = os.environ.get('MPESA_SHORTCODE', '174379')
    passkey = os.environ.get('MPESA_PASSKEY', '')
    timestamp = get_timestamp()
    password = get_password(shortcode, passkey, timestamp)

    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    payload = {
        'BusinessShortCode': shortcode,
        'Password': password,
        'Timestamp': timestamp,
        'CheckoutRequestID': checkout_request_id
    }

    try:
        resp = requests.post(
            'https://sandbox.safaricom.co.ke/mpesa/stkpushquery/v1/query',
            headers=headers,
            json=payload,
            timeout=30
        )
        return resp.json()
    except Exception as e:
        return {'error': str(e)}
