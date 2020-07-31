import hashlib
from paywix.utils import payu_config, payu_url_generator
from paywix.exceptions import AccessModeException
from paywix.decorators import validate_params
import requests
from urllib3.request import urlencode

refund_api_commands = ['getRefundDetails', 'getRefundDetailsByPayment']


class Payu():

    def __init__(self, merchant_key, merchant_salt, s_url, f_url, mode='TEST',
                 auth_header=None):
        if mode.lower() not in ['test', 'live']:
            raise AccessModeException(mode)
        self.merchant_key = merchant_key
        self.merchant_salt = merchant_salt
        self.success_url = s_url
        self.failure_url = f_url
        self.base_url = payu_config.get(mode.lower(), 'test')
        self.auth_header = auth_header
        self.mode = mode

    def generate_txnid(self, prefix=None, limit=20):
        hash_object = hashlib.sha256(b'randint(0,20)')
        txnid = f'{prefix} {hash_object.hexdigest()[0:limit]}'
        return txnid

    def generate_hash(self, hash_string):
        hash_value = hashlib.sha512(
            hash_string.encode('utf-8')).hexdigest().lower()
        return hash_value

    @validate_params('payu_request', 'payu', 'transaction')
    def transaction(self, **kwargs):
        kwargs.update({'key': self.merchant_key})
        hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1\
            |udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string = ''
        hashVarsSeq = hashSequence.split('|')
        for hash_str in hashVarsSeq:
            try:
                hash_string += str(kwargs[hash_str])
            except Exception:
                hash_string += ''
            hash_string += '|'
        hash_string += self.merchant_salt
        data = kwargs
        data.update({
            'hashh': self.generate_hash(hash_string),
            'merchant_key': self.merchant_key,
            'surl': self.success_url,
            'furl': self.failure_url,
            'hash_string': hash_string,
            'service_provider': 'payu_paisa',
            'action': self.base_url
        })
        return data

    def verify_transaction(self, response_data):
        results = {}
        status = response_data.get('status')
        first_name = response_data.get('firstname')
        amount = response_data.get('amount')
        txnid = response_data.get('txnid')
        response_key = response_data.get('key')
        product_info = response_data.get('productinfo')
        email = response_data.get('email')
        response_hash = response_data.get("hash")
        add_charge = response_data.get('additionalCharges')
        hash_string = ""
        if add_charge:
            hash_string += f'{add_charge}|'

        hash_string += f'{self.merchant_salt}|{status}|||||||||||{email}|{first_name}|{product_info}|{amount}|{txnid}|{response_key}'
        generated_hash = self.generate_hash(hash_string)
        results.update({"return_data": response_data})
        results.update({
            'hash_string': hash_string,
            'generated_hash': generated_hash,
            'recived_hash': response_hash,
            'hash_verified': generated_hash == response_hash
        })
        return results

    def generate_header(self):
        header = {}
        header.update({
            "authorization": self.auth_header,
            "content-type": "application/json",
            "cache-control": "no-cache"
        })
        return header

    def make_query_params(self, data):
        query_params = urlencode(data)
        return query_params

    def make_request(self, command, required_data, optionals=None):
        api_mode = {"test": "api_test", "live": "api_live"}
        mode = api_mode.get(self.mode.lower())
        headers = self.generate_header()
        required_data.update({'key': self.merchant_key})
        service_url = payu_url_generator(
            command, mode, refund_api=True if command in refund_api_commands else False)
        service_url = service_url.format(**required_data)
        if optionals:
            query_params = self.make_query_params(optionals)
            service_url += query_params
        try:
            response = requests.post(service_url, headers=headers)
            # Consider any status other than 2xx an error
            if not response.status_code // 100 == 2:
                return {"status": response.status_code,
                        "message": f"Error: Unexpected response {response.content}"
                        }
            json_obj = response.json()
            return {"status": response.status_code, "result": json_obj}
        except requests.exceptions.RequestException as e:
            return {"status": 500, "message": f"Error: {e}"}

    def getPaymentResponse(self, required_data, optionals=None):
        if optionals is None:
            optionals = {}
        if not required_data.get('ids'):
            raise Exception("Parameter id's missing in required_data")
        required_data['ids'] = "|".join(required_data['ids'])
        response = self.make_request(
            "getPaymentResponse", required_data, optionals=optionals)
        return response

    def chkMerchantTxnStatus(self, required_data):
        if not required_data.get('ids'):
            raise Exception("Parameter id's missing in required_data")
        required_data['ids'] = "|".join(required_data['ids'])
        response = self.make_request(
            "chkMerchantTxnStatus", required_data)
        return response

    def refundPayment(self, required_data, optionals=None):
        if optionals is None:
            optionals = {}
        for key in ['payu_id', 'amount']:
            if not required_data.get(key):
                raise Exception(
                    f"Mandatory {key} params missing in required_data")
        response = self.make_request(
            'refundPayment', required_data, optionals=optionals)
        return response

    def getRefundDetails(self, required_data):
        if not required_data.get('refund_id'):
            raise Exception(
                "Mandatory refund_id params missing in required_data")
        response = self.make_request(
            'getRefundDetails', required_data)
        return response

    def getRefundDetailsByPayment(self, required_data):
        if not required_data.get('payu_id'):
            raise Exception(
                "Mandatory payu_id params missing in required_data")
        response = self.make_request(
            'getRefundDetailsByPayment', required_data)
        return response
