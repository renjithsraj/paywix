import hashlib
from django.conf import settings
p = getattr(settings, 'PAYU_CONFIG', {})


class PAYU(object):
    def __init__(self):

        urls_dict = {
            "TEST": "https://sandboxsecure.payu.in/_payment",
            "LIVE": "https://secure.payu.in/_payment"
        }
        print ("the p", p)
        for param in ['merchant_key', 'merchant_salt', 'mode',
                      'success_url', 'failure_url']:
            if not p.get(param):
                raise Exception("{0} not included in the PAYUCONFIG".format(
                    param))
        self.base_url = urls_dict.get(p.get('mode', 'TEST'))
        self.mechent_key = p.get('merchant_key')
        self.salt = p.get('merchant_salt')
        self.key = p.get('merchant_key')
        self.success_url = p.get('success_url')
        self.failure_url = p.get('failure_url')
        self.required_fields = [
            'txnid', 'amount', 'productinfo', 'firstname', 'email'
        ]

    def generate_txnid(self):
        hash_object = hashlib.sha256(b'randint(0,20)')
        txnid = hash_object.hexdigest()[0:20]
        return txnid

    def generate_hash(self, hash_string):
        hashh = hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        return hashh

    def initate_transaction(self, data):
        for item in self.required_fields:
            if not data.get(item):
                return Exception("{0} missing in the data".format(item))
        data['key'] = self.mechent_key
        hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string = ''
        hashVarsSeq = hashSequence.split('|')
        for i in hashVarsSeq:
            try:
                hash_string += str(data[i])
            except Exception:
                hash_string += ''
            hash_string += '|'
        hash_string += self.salt
        # Generate Hash
        data.update({
            'hashh': self.generate_hash(hash_string),
            'merchant_key': self.mechent_key,
            'surl': self.success_url,
            'furl': self.failure_url,
            'hash_string': hash_string,
            'service_provider': 'payu_paisa',
            'action': self.base_url
        })
        return data

    def check_hash(self, data):
        response = {}
        for item in data:
            data[item] = data[item][0]
        s, f, m, t, k, p, e = data.get("status"), data.get("firstname"), \
            data.get("amount"), data.get("txnid"), data.get("key"), \
            data.get("productinfo"), data.get("email")
        posted_hash = data.get("hash")
        if data.get('additionalCharges'):
            additional_charges = data["additionalCharges"]
            ret_hash_seq = additional_charges + '|' + self.salt + '|' + s + '|||||||||||' + e + '|' + f + '|' + p + '|' + m + '|' + t + '|' + k
        else:
            ret_hash_seq = self.salt + '|' + s + '|||||||||||' + e + '|' + f + '|' + p + '|' + m + '|' + t + '|' + k
        hashh = hashlib.sha512(
            ret_hash_seq.encode('utf-8')).hexdigest().lower()
        return response.update({
            'data': data,
            'hash_string': ret_hash_seq,
            'generated_hash': hashh,
            'recived_hash': posted_hash,
            'verify_token': posted_hash == hashh
        })
