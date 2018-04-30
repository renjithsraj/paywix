# Standard Library
import hmac
import base64
import hashlib
import requests
from django.conf import settings


CASHFREE_APPID = getattr(settings, 'CASHFREE_APPID', '')
CASHFREE_SECRETKEY = getattr(settings, 'CASHFREE_SECRETKEY', '')
CASHFREE_MODE = getattr(settings, 'CASHFREE_MODE', '')
URL_DATA = {"LIVE": "https://api.gocashfree.com/{0}", "TEST": "https://test.gocashfree.com/{0}"}
CASHFREE_SUCCESS_URL = getattr(settings, 'CASHFREE_SUCCESS_URL', '/')
CASHFREE_FAILURE_URL = getattr(settings, 'CASHFREE_FAILURE_URL', '/')
CASHFREE_PAYMENT_BY_URL = getattr(settings, 'CASHFREE_PAYMENT_BY_URL', False)

CASHFREE_ENDPOINTS = {
    "create_order": "api/v1/order/create",
    'txn_status': "/api/v1/order/info/status"
}


# Settings parameter validator
def settings_validator():
    for settings_parm in [CASHFREE_APPID, CASHFREE_SECRETKEY, CASHFREE_MODE, CASHFREE_SUCCESS_URL,
                          CASHFREE_FAILURE_URL]:
        if not bool(settings_parm):
            raise Exception("Missing Mandatory {0} field in settings.py".format(settings_parm))


# Signature for payment link
def generate_signature(data):
    sorted_keys = sorted(data)
    signature_data = ""
    for key in sorted_keys:
        signature_data += key + data[key]
    message = bytes(signature_data).encode('utf-8')
    secret = bytes(settings.CASHFREE_SECRETKEY).encode('utf-8')
    signature = base64.b64encode(
        hmac.new(secret, message, digestmod=hashlib.sha256).digest())
    return signature


# Generate token for cashfree pop up and other services
def generate_token(data, secretKey):
    data['returnUrl'] = ""
    data = "appId=" + data['appId'] + "&orderId=" + data['orderId'] + \
           "&orderAmount=" + data['orderAmount'] + \
           "&returnUrl=" + data['returnUrl'] + \
           "&paymentModes=" + data.get('paymentModes', "")
    message = bytes(data).encode('utf-8')
    secret = bytes(secretKey).encode('utf-8')
    paymentToken = base64.b64encode(
        hmac.new(secret, message, digestmod=hashlib.sha256).digest())
    return paymentToken

# Initiate Cashfree transaction
def initiate(order_id,
             phone,
             email,
             customer_name,
             amount,
             order_note,
             return_url=None):
    settings_validator()
    data = {
        'appId': CASHFREE_APPID,
        'orderId': order_id,
        'orderAmount': str(amount),
        'orderNote': order_note,
        'customerName': customer_name,
        'customerPhone': phone,
        'customerEmail': email,
        'returnUrl': return_url,
        'notifyUrl': return_url,
    }
    if CASHFREE_PAYMENT_BY_URL:
        start_url = None
        signature = generate_signature(data)
        data.update({"signature": signature, "secretKey": CASHFREE_SECRETKEY})
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        order_url = URL_DATA[CASHFREE_MODE].format(CASHFREE_ENDPOINTS['create_order'])
        request_resp = requests.post(url=order_url, data=data, headers=headers).json()
        if request_resp['paymentLink']:
            start_url = request_resp['paymentLink']
        resp = {"order_url": start_url, "provider": "CASHFREE", "data": data}
    else:
        resp = {
            "provider": "CASHFREE",
            "data": {
                "return_url": return_url,
                "txn_id": order_id,
                "email": email,
                "phone": phone,
                "merchant": CASHFREE_APPID,
                "merchant_key": CASHFREE_APPID,
                "success_url": CASHFREE_SUCCESS_URL,
                "failure_url": CASHFREE_FAILURE_URL,
                "order_hash": generate_token(data, CASHFREE_SECRETKEY),
                "first_name": customer_name,
                "amount": str(amount),
                "product_name": order_note,
            }
        }
    return resp

# Verify cashfree payment response Hash
def verify_signature(pg_data):
    settings_validator()
    data_string = pg_data['orderId'] + pg_data['orderAmount'] + \
                  pg_data['referenceId'] + pg_data['txStatus'] + \
                  pg_data['paymentMode'] + pg_data['txMsg'] + pg_data['txTime']
    message = bytes(data_string).encode('utf-8')
    secret = bytes(CASHFREE_SECRETKEY).encode('utf-8')
    computed_signature = base64.b64encode(
        hmac.new(secret, message, digestmod=hashlib.sha256).digest())
    return (pg_data.get('signature') == computed_signature, data_string,
            computed_signature)


def generate_checksum(callback):
    checksum = generate_signature(callback)
    return checksum
