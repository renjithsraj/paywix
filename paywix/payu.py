import hashlib
from django.conf import settings

PAYU_KEY = getattr(settings, 'PAYU_KEY', '3o6jgxhp')
PAYU_SALT = getattr(settings, 'PAYU_SALT', '67bAgZX1B3')
PAYU_SUCCESS_URL = getattr(settings, 'PAYU_SUCCESS_URL', '/')
PAYU_FAILURE_URL = getattr(settings, 'PAYU_FAILURE_URL', '/')
PAYU_MODE = getattr(settings, 'PAYU_MODE', 'TEST')

PAYMENT_URLS = {
    "LIVE": "https://secure.payu.in/_payment",
    "TEST": "https://sandboxsecure.payu.in/_payment"
}
SERVICE_PROVIDER = "payu_paisa"


def initiate(payu_data):
    hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
    hash_string = ""
    hashVarsSeq = hashSequence.split('|')
    payu_data['key'] = PAYU_KEY
    response_data = {}
    payu_data['amount'] = str(payu_data['amount'])
    for i in hashVarsSeq:
        try:
            hash_string += str(payu_data[i])
            response_data[i] = payu_data[i]
        except Exception:
            hash_string += ''
        hash_string += '|'
    response_data.update({
        'key': PAYU_KEY, 'surl': PAYU_SUCCESS_URL,
        'furl': PAYU_FAILURE_URL,
        'phone': payu_data['phone'], 'amount': str(payu_data['amount'])})

    hash_string += PAYU_SALT
    hashh = hashlib.sha512(hash_string.encode("utf-8")).hexdigest().lower()
    data = {
        "posted": response_data,
        "hashh": hashh,
        "MERCHANT_KEY": PAYU_KEY,
        "txnid": payu_data['txnid'],
        "hash_string": hash_string,
        "action": PAYMENT_URLS[PAYU_MODE],
        "service_provider": SERVICE_PROVIDER
    }
    return data


def check_hash(data):
    status = data.get("status")
    firstname = data.get("firstname")
    amount = data.get("amount")
    txnid = data.get("txnid")
    posted_hash = data.get("hash")
    key = data.get("key")
    productinfo = data.get("productinfo")
    email = data.get("email")
    if data.get('additionalCharges'):
        additionalCharges = data["additionalCharges"]
        retHashSeq = additionalCharges + '|' + PAYU_SALT + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
    else:
        retHashSeq = PAYU_SALT + '|' + status + '|||||||||||' + email + '|' + firstname + '|' + productinfo + '|' + amount + '|' + txnid + '|' + key
        hashh = hashlib.sha512(retHashSeq.encode('utf-8')).hexdigest().lower()
    return (hashh == posted_hash, retHashSeq, hashh)
