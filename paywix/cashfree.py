import hmac
import base64
import hashlib
import uuid

from django.conf import settings
from paywix.decorators import validate_params


cashfree_config = getattr(settings, 'CASHFREE_CONFIG', {})


class Cashfree(object):
    """
    To know the available currency's access the function.
    from paywix.utils import get_casfree_currency_data
    currency_data = get_casfree_currency_data()
    """

    def __init__(self, app_id, secret_key, return_url, notify_url=None,
                 currency='INR', mode="TEST"):
        self.appId = app_id
        self.secretKey = secret_key
        self.returnUrl = return_url
        self.notifyUrl = notify_url if notify_url else return_url
        self.orderCurrency = currency

    def generate_signature(self, postData):
        sortedKeys = sorted(postData)
        signatureData = ""
        for key in sortedKeys:
            signatureData += key + postData[key]
        message = signatureData.encode('utf-8')
        secret = self.secretKey.encode('utf-8')
        signature = base64.b64encode(hmac.new(secret, message,
            digestmod=hashlib.sha256).digest()).decode("utf-8")
        return signature

    @validate_params('cashfree_request', 'cashfree', 'transaction')
    def initiate_transaction(self, data):
        for req_field in self.required_params:
            if not data.get(req_field):
                raise KeyError("{0} not found in PostData".format(req_field))
        postData = {
            "appId": self.appId,
            "orderId": data.get('order_id'),
            "orderAmount": data.get('amount'),
            "orderCurrency": self.order_currency,
            "orderNote": data.get('note'),
            "customerName": data.get('name'),
            "customerPhone": data.get('phone'),
            "customerEmail": data.get('email'),
            "returnUrl": self.returnUrl,
            "notifyUrl": self.notifyUrl
        }
        signature = self.generate_signature(postData)
        postData.update(
            {'signature': signature, 'action_url': self.payment_url})
        return postData

    def verify_hash(self, response_data):
        signatureData = ""
        signatureData = response_data['orderId'] + response_data['orderAmount'] + \
            response_data['referenceId'] + response_data['txStatus'] + \
            response_data['paymentMode'] + response_data['txMsg'] + \
            response_data['txTime']

        message = signatureData.encode('utf-8')
        secret = self.secretKey.encode('utf-8')
        res_signature = response_data.get('signature')
        c_signature = base64.b64encode(hmac.new(secret, message,
                                                digestmod=hashlib.sha256).digest()).decode('utf-8')
        response_data.update({"verify_hash": res_signature == c_signature,
                              "computed_hash": c_signature})
        return response_data
