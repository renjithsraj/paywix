from paywix import Checksum
from django.conf import settings

paytm_data = getattr(settings, 'PAYTM_CONFIG', {})


class PayTm(object):

    def __init__(self):
        urls_dict = {
            "LIVE": "https://securegw.paytm.in/theia/processTransaction",
            "TEST": "https://securegw-stage.paytm.in/theia/processTransaction"
        }

        for req_item in ['merchant_key', 'merchant_id', 'callback_url', 'website']:
            if not paytm_data.get(req_item):
                raise KeyError("{0} Not found in PAYTM_CONFIG".format(req_item))
        self.merchant_id = paytm_data['merchant_id']
        self.merchant_key = paytm_data['merchant_key']
        self.callback_url = paytm_data['callback_url']
        self.website = paytm_data['website']
        self.txn_url = urls_dict.get(paytm_data['mode'], 'TEST')
        self.industry_type = "Retail"

    def initiate_transaction(self, data_dict):
        data_dict.update({"MID": self.merchant_id,
                           "WEBSITE": self.website,
                           "INDUSTRY_TYPE_ID": self.industry_type,
                           "CHANNEL_ID": "WEB",
                           "CALLBACK_URL": self.callback_url})
        param_dict = data_dict
        param_dict["CHECKSUMHASH"] = Checksum.generate_checksum(data_dict, self.merchant_key)
        param_dict.update({"action_url": self.txn_url})
        return param_dict

    def id_generater(self):
        return Checksum.__id_generator__()

    def verify_hash(self, data_dict):
        response = {}
        verify_hash = Checksum.verify_checksum(data_dict,
                        self.merchant_key, data_dict["CHECKSUMHASH"])
        response.update({"return_data": data_dict, "verify_hash": verify_hash})
        return response



