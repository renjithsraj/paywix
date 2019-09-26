import hmac
import base64
import hashlib
import  uuid

from django.conf import  settings
cashfree_config = getattr(settings, 'CASHFREE_CONFIG', {})

class Cashfree(object):
    cashfree_links = {
        "LIVE": "https://www.cashfree.com/checkout/post/submit",
        "TEST": "https://test.cashfree.com/billpay/checkout/post/submit"
    }

    def __init__(self):
        if not cashfree_config:
            raise ValueError("Please Include CASHFREE_CONFIG in settings")
        for config_item in ['app_id', 'secret_key', 'return_url', 'currency']:
            if not cashfree_config.get(config_item):
                raise KeyError("{0} missing in the CASHFREE_CONFIG".format(config_item))
        self.appId = cashfree_config.get('app_id')
        self.secretKey = cashfree_config.get('secret_key')
        self.returnUrl = cashfree_config.get('return_url')
        self.notifyUrl = cashfree_config.get('notify_url', self.returnUrl)
        self.order_currency = cashfree_config.get('currency', 'INR')
        self.payment_url = self.cashfree_links.get(cashfree_config.get('mode'), 'TEST')
        self.required_params = ['amount', 'order_id', 'name', 'email', 'phone', 'note']


    def generate_txnid(self):
        order_id = uuid.uuid4()
        return order_id


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
        postData.update({'signature': signature, 'action_url': self.payment_url})
        return  postData


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
        response_data.update({"verify_hash": res_signature==c_signature,
                              "computed_hash": c_signature})
        return response_data

