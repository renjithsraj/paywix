from django.conf import settings
import datetime
import hashlib

class PAYU(object):
    
    def __init__(self):
        self.test_url = "https://sandboxsecure.payu.in/_payment"
        self.secure_url = 'https://secure.payu.in/_payment'
        self.base_url = self.test_url if settings.PAYMENT_MODE == 'TEST' else self.secure_url
        self.mechent_key = settings.PAYU_MERCHANT_KEY
        self.salt = settings.PAYU_SALT
        self.key = settings.PAYU_KEY
        self.success_url = settings.PAYU_SUCCESS_URL
        self.failure_url = settings.PAYU_FAILURE_URL

    def generate_hash(self, hash_string):
        hashh= hashlib.sha512(hash_string.encode('utf-8')).hexdigest().lower()
        return hashh
    
    def initate_transaction(self, data):
        data['key'] = self.mechent_key
        hashSequence = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|udf6|udf7|udf8|udf9|udf10"
        hash_string=''
        hashVarsSeq=hashSequence.split('|')
        for i in hashVarsSeq:
            try:
                hash_string+=str(data[i])
            except Exception:
                hash_string+=''
            hash_string+='|'
        hash_string+=self.salt
        # Generate Hash
        data.update({ 
            'hash': self.generate_hash(hash_string), 
            "": ""})



        hashh = 
        data['merchant_key'] = self.mechent_key
        data['surl'] = self.success_url
        data['furl'] = self.failure_url
        data['hashh'] = hashh
        data['hash_string'] = hash_string
        data['service_provider'] = 'payu_paisa'
        data['action'] = self.base_url
        return data
    
    def check_hash(self, data):
        response = {}
        for item in data:
            data[item] = data[item][0]
        s, f, m, t, k, p,e = data.get("status"), data.get("firstname"), 
                data.get("amount"), data.get("txnid"), data.get("key"), 
                data.get("productinfo") , data.get("email")
        posted_hash = data.get("hash")
        if data.get('additionalCharges'):
            additional_charges = data["additionalCharges"]
            ret_hash_seq = additional_charges + '|' + self.salt + '|' + s + '|||||||||||' + e + '|' + f + '|' + p + '|' + m + '|' + t + '|' + k
        else:
            ret_hash_seq = self.salt + '|' + s + '|||||||||||' + e + '|' + f + '|' + p + '|' + m + '|' + t + '|' + k
        hashh = hashlib.sha512(ret_hash_seq.encode('utf-8')).hexdigest().lower()
        return response.update{
            'data': data,
            'hash_string': ret_hash_seq,
            'generated_hash': hashh,
            'recived_hash': posted_hash,
            'verify_token': posted_hash == hashh
        })