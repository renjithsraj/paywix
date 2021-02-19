from paywix.paytm_checksum import PaytmChecksum
import requests as rq
import json


PAYTM_CONFIG = {
    "test": "https://securegw-stage.paytm.in/theia",
    "production": "https://securegw.paytm.in/theia",
    "order": {
        "test": "https://securegw-stage.paytm.in/order/process",
        "production": "https://securegw.paytm.in/order/process"
    }
}


class Paytm(object):

    def __init__(self, mid, key, mode='test'):
        self.mid = mid
        self.mode = mode
        self.key = key
        if self.mode.lower() not in ['test', 'production']:
            raise ValueError(f"{self.mode} not in list")
        self.default_header = {"Content-type": "application/json"}

    def __make_request(self, url, data, headers, method='post'):
        data = self.__make_data(data)
        if method == 'post':
            resp = rq.post(url, data=data, headers=headers).json()
        else:
            resp = rq.get(url, data=data, headers=headers).json()
        return resp

    def __make_data(self, data):
        return json.dumps(data)

    def init_transaction(self, data):
        data['body']['mid'] = self.mid
        paytm_checksum = PaytmChecksum()
        checksum = paytm_checksum.generate_signature(
            self.__make_data(data['body']), self.key)
        data['head'] = {
            "signature": checksum
        }
        _url = f"/api/v1/initiateTransaction?mid={self.mid}&orderId={data['body']['orderId']}"
        url = f"{PAYTM_CONFIG[self.mode]}{_url}"
        resp = self.__make_request(url, data, self.default_header)
        response = {
            'action_url': f"{PAYTM_CONFIG[self.mode]}/api/v1/showPaymentPage?mid={self.mid}&orderId={data['body']['orderId']}",
            'mid': self.mid,
            'orderId': data['body']['orderId'],
            'txnToken': resp['body']['txnToken'],
            'paytm_resp': resp
        }
        return response

    def generate_checkout_html(self, param_dict):
        ''' Generating HTML payment form  for paytm payment '''
        HTML = f""" 
            <html>
                <head>
                    <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
                    <title>Paytm Secure Online Payment Gateway</title>
                </head>
                <body>
                    <table align='center'>
                        <tr>
                            <td><STRONG>Transaction is being processed,</STRONG></td>
                        </tr>
                        <tr>
                            <td><font color='blue'>Please wait ...</font></td>
                        </tr>
                        <tr>
                            <td>(Please do not press 'Refresh' or 'Back' button</td>
                        </tr>
                    </table>
                     <form method="post" action={PAYTM_CONFIG['order'][self.mode]} name="paytm">
                        <table border="1">
                            <tbody>"""
        ''' Take inputs from data dict and appending dynamically into the input fields '''
        for key, value in param_dict.items():
            HTML += f"<input type='hidden' name='{key}' value='{value}'>"

        HTML += """
                        </tbody>
                    </table>
                    <script type="text/javascript">
                        document.paytm.submit();
                    </script>
                </form>
            </body>
            </html>"""
        return HTML

    def checkout_data(self, data, is_html=None):
        """
        Args: data:
            "MID" : "YOUR_MID_HERE",
            "WEBSITE" : "YOUR_WEBSITE_HERE",
            "INDUSTRY_TYPE_ID" : "YOUR_INDUSTRY_TYPE_ID_HERE",
            "CHANNEL_ID" : "YOUR_CHANNEL_ID",
            "ORDER_ID" : "YOUR_ORDER_ID",
            "CUST_ID" : "CUSTOMER_ID",
            "TXN_AMOUNT" : "ORDER_TRANSACTION_AMOUNT",
            "CALLBACK_URL" : "YOUR_CALLBACK_URL",
            "MOBILE_NO" : "CUSTOMER_MOBILE_NUMBER",
            "EMAIL" : "CUSTOMER_EMAIL",   
        """
        required_params = [
            'website', 'industry_type_id', 'channel_id', 'order_id', 'cust_id',
            'txn_amount', 'callback_url'
        ]
        for param in required_params:
            if param not in data and data.get(param):
                raise KeyError(f"{param} is required to proceed checkout data")
        params_data = {k.upper(): v for k, v in data.items()}
        params_data['MID'] = self.mid
        checksum = PaytmChecksum()
        params_data['CHECKSUMHASH'] = checksum.generate_signature(
            params_data, self.key)
        if is_html is True:
            return self.generate_checkout_html(params_data)
        return params_data

    def verify_response(self, data):
        ''' Verify Payment response
        check the paytm hash with calculated hash
        '''
        resp = data
        if data.get('CHECKSUMHASH'):
            checksum = PaytmChecksum()
            checksum_data = checksum.verify_signature(
                data, self.key, data['CHECKSUMHASH'])
            resp.update(
                checksum_data
            )
        resp = {k.lower(): v for k, v in resp.items()}
        return resp
