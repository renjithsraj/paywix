from paywix.exceptions import ModeException
from paywix.decorators import validate_params
from paywix.config import PAYU_CONFIGS
import hashlib
import logging
import requests
from urllib import parse


class Payu:

    # Hash Sequence for transaction
    __HASH_SEQUENCE = "key|txnid|amount|productinfo|firstname|email|udf1|udf2|udf3|udf4|udf5|||||"
    __RESPONSE_SEQUENCE = "salt|status||||||udf5|udf4|udf3|udf2|udf1|email|firstname|productinfo|amount|txnid"
    __API_HASH_SEQUENCE = "key|command|var1"

    def __init__(self, merchant_key, merchant_salt, mode='Test'):

        self.key = merchant_key
        self.salt = merchant_salt
        self.mode = mode.lower()
        if self.mode not in ("test", "live"):
            raise ModeException(self.mode)

    def __repr__(self):
        return f'Payu({self.key}, {self.salt}, {self.mode})'

    def generate_hash(self, *args, **kwargs):
        """
            Generate hash for requested arguments
        """
        kwargs.update({'key': self.key})
        hash_seq_list = self.__HASH_SEQUENCE.split('|')
        hash_string = ""
        for hash_str in hash_seq_list:
            try:
                hash_string += str(kwargs[hash_str])
            except Exception:
                hash_string += ''
            hash_string += '|'
        hash_string += self.salt
        hash_value = hashlib.sha512(
            hash_string.encode('utf-8')).hexdigest().lower()
        logging.info("Hash generation has completed")
        return hash_value

    def make_html(self, data):
        """
            Reurn HTML string based on requested data
        """
        inputs_string = ""
        request_payload = ['key', 'txnid', 'productinfo',
                           'amount', 'email', 'firstname', 'lastname', 'surl',
                           'surl', 'furl', 'phone', 'hash', 'udf1', 'udf2', 'udf3',
                           'udf4', 'udf5'
                           ]
        for input_val in request_payload:
            if data.get(input_val):
                val = f'<input type="hidden" name="{input_val}" value="{data.get(input_val)}" />'
                inputs_string += val

        submit_form = "window.onload = function(){document.forms['payuform'].submit()}"
        html_tag = \
            f"""
                <html>
                    <body>
                        <form action='{data.get('action')}' method='post' id='payuform'>
                            {inputs_string}
                        </form>
                        <script>
                        {submit_form}
                        </script>
                    </body>
                </html>
            """
        return html_tag

    @validate_params('payu', 'transaction')
    def transaction(self, *args, **kwargs):
        """
            Transaction Initialization for requested parameters.
            action: transaction
            required-kwargs:  ['amount', 'email', 'productinfo', 'furl', 'txnid',
                            'firstname', 'phone']

            if kwargs['txn_type'] == 'form'
                return html forms with requested data
            else:
                return url for the requested payload.
        """
        hash_value = self.generate_hash(*args, **kwargs)
        __required_items = ['amount', 'email', 'productinfo', 'furl', 'txnid',
                            'firstname', 'phone', 'surl', 'phone']
        for req_item in __required_items:
            if not kwargs.get(req_item):
                raise KeyError(f" {req_item} not found in {kwargs}")
        kwargs['key'] = self.key
        kwargs['hash'] = hash_value
        kwargs['action'] = PAYU_CONFIGS[self.mode]
        return kwargs

    def __generate_response_hash(self, *args, **kwargs):
        kwargs['salt'] = self.salt
        kwargs['key'] = self.key
        hash_seq_list = self.__RESPONSE_SEQUENCE.split('|')
        add_charge = kwargs.get('additionalCharges')
        hash_string = ""
        for hash_str in hash_seq_list:
            hash_string += f"{str(kwargs.get(hash_str, ''))}|"
        hash_string += f'{self.key}'
        if add_charge:
            hash_string = f'{add_charge}|{hash_string}'
        generated_hash = hashlib.sha512(
            hash_string.encode('utf-8')).hexdigest().lower()
        return hash_string, generated_hash

    def __error_codes(self, reqstd_code):
        error_codes = PAYU_CONFIGS['error_codes']
        return error_codes.get(reqstd_code, "None")

    def __bank_code(self, requstd_code):
        bank_codes = PAYU_CONFIGS['payment_modes']
        return bank_codes.get(requstd_code)

    def check_transaction(self, *args, **kwargs):
        """
            Verify Transaction from Payu.
            Check the payment gateway response.
        """
        hash_string, hash_value = self.__generate_response_hash(
            *args, **kwargs)
        response_hash = kwargs.get('hash')
        hash_response = {
            "hash_string": hash_string,
            "hash_value": hash_value,
            "is_hash_verified": response_hash == hash_value,
        }
        payment_response = {
            "mihpayid": kwargs.get('mihpayid'),
            "status": kwargs.get("status"),
            "error": self.__error_codes(kwargs.get('error')),
            "mode": kwargs.get('mode'),
            "bank_code": self.__bank_code(kwargs.get('bankcode')),
            "payment_source": kwargs.get('payment_source'),
            "transaction_msg": kwargs.get('field9', kwargs.get("status")),
            "transaction_id": kwargs.get('txnid')
        }
        final_response = {
            "hash_response": hash_response,
            "all_response": kwargs,
            "payment_response": payment_response
        }

        return final_response

    def __payload_encode(self, **kwargs):
        return parse.urlencode(kwargs)

    def __api_hash(self, *args, **kwargs):

        hash_seq_list = self.__API_HASH_SEQUENCE.split('|')
        hash_string = ""
        for hash_str in hash_seq_list:
            hash_string += f"{str(kwargs.get(hash_str, ''))}|"
        hash_string += f'{self.salt}'
        generated_hash = hashlib.sha512(
            hash_string.encode('utf-8')).hexdigest().lower()
        return hash_string, generated_hash

    def __make_request(self, method="POST", **kwargs):
        kwargs['key'] = self.key
        kwargs['salt'] = self.salt
        api_hash_string, api_hash = self.__api_hash(**kwargs)
        kwargs['hash'] = api_hash
        try:
            headers = {
                "Accept": "application/json",
                "Content-Type": "application/x-www-form-urlencoded"
            }
            payload = self.__payload_encode(**kwargs)
            url = PAYU_CONFIGS[f'api_{self.mode}']
            response = requests.request(
                method, url, data=payload, headers=headers)
            return response.json()
        except requests.exceptions.HTTPError as http_error:
            raise Exception(f"Http Error: {str(http_error)}")
        except requests.exceptions.ConnectionError as conn_error:
            raise Exception(f"Error Connecting: {str(conn_error)}")
        except requests.exceptions.Timeout as timeout_error:
            raise Exception(f"Timeout Error: {str(timeout_error)}")
        except requests.exceptions.RequestException as req_error:
            raise Exception(f"Timeout Error: {str(req_error)}")
        except Exception as e:
            raise Exception(f"Unknown error occurred: {str(e)}")

    def verify_payment(self, *args, **kwargs):
        """
            Verify Payment
            This API gives you the status of the transaction.We recommend
            to use this API to
            reconcile with PayU’s database once you receive the response.
        """
        if len(kwargs.get('transaction_id')) == 0:
            raise KeyError(
                " Requested data doesn't contains required field: transaction_id")
        kwargs['command'] = "verify_payment"
        kwargs['var1'] = "|".join(kwargs.pop('transaction_id'))
        response = self.__make_request(**kwargs)
        return response

    def check_payment(self, *args, **kwargs):
        """
            Check Payment
            This API gives you the status of the transaction similar to verify_payment API.
            The only difference is that the input parameter in this
            API (i.e. var1) is the PayUID (MihpayID) generated at PayU’s end
            whereas the input parameter in verify_payment API is the TxnID (Transaction ID generated at your end).
        """
        if not kwargs.get('payment_id'):
            raise KeyError(
                f" Requested data doesn't contains required field: payment_id")
        kwargs['command'] = "check_payment"
        kwargs['var1'] = kwargs.pop('payment_id')
        response = self.__make_request(**kwargs)
        return response

    def get_wsonline_response(self, *args, **kwargs):
        """
            This API is used to get the transaction response sent on surl/furl.
        """
        if not kwargs.get('transaction_id'):
            raise KeyError(
                " Requested data doesn't contains required field: transaction_id")
        kwargs['command'] = "get_ws_response"
        kwargs['var1'] = kwargs.pop('transaction_id')
        response = self.__make_request(**kwargs)
        return response

    def get_transaction_details(self, *args, **kwargs):
        """
            This API is used to extract the transaction details between two given time periods.
            The API takes the input as two dates (date_from = initial and date_to = final), between which
            the transaction details are needed.

            date_from & date_to:
            This parameter must contain the starting date
            (from when the transaction details are needed) in YYYY-MM-DD format.
        """

        for key in ['date_from', 'date_to']:
            if not kwargs.get(key):
                raise KeyError(
                    f"To get transaction details required parameter is missing {key}")

        kwargs['command'] = "get_Transaction_Details"
        kwargs['var1'] = kwargs.pop('date_from')
        kwargs['var2'] = kwargs.pop('date_to')
        response = self.__make_request(**kwargs)
        return response

    def get_transaction_info(self, *args, **kwargs):
        """
            This API works exactly the same way as get_Transaction_Details API.
            The only enhancement is that this API can take input as the exact time
            in terms of minutes and seconds also, date_time_from and date_time_to
            are starting & end dates
            of transactions with time, respectively.

            This parameter must contain the starting Time
            (from when the transaction details are needed) in YYYY-MM-DD HH:MM:SS format
        """
        for key in ['date_time_from', 'date_time_to']:
            if not kwargs.get(key):
                raise KeyError(
                    f"To get transaction details required parameter is missing {key}")

        kwargs['command'] = "get_transaction_info"
        kwargs['var1'] = kwargs.pop('date_time_from')
        kwargs['var2'] = kwargs.pop('date_time_to')
        response = self.__make_request(**kwargs)
        return response

    def get_tdr(self, *args, **kwargs):
        """
            This API is used to get the TDR value of a transaction with PayU. It is a simple API
            for which you need to provide the PayU ID of the transaction
            as input and the TDR value is returned
            to the output.
        """
        if len(kwargs.get('payment_id')) == 0:
            raise KeyError(
                " Requested data doesn't contains required field: payment_id")
        kwargs['command'] = "get_TDR"
        kwargs['var1'] = kwargs.get('payment_id')
        response = self.__make_request(**kwargs)
        return response

    def refund(self, *args, **kwargs):
        """
            The Cancel Refund Transaction API (cancel_refund_transaction) can be used for
            the following purposes:
            Cancel a transaction that is in ‘auth’ state at the moment
            Refund a transaction that is in a ‘captured’ state at the moment.
            In this API: var1 is the Payu ID (mihpayid) of the transaction, var2 should
            contain the Token ID (unique token from the merchant), and var3 parameter s
            hould contain the amount which needs to be refunded.

            payment_id: This parameter must contain the Payu ID (mihpayid) of the transaction.
            refund_id: This parameter must contain the Token ID
                (unique token from the merchant) for the refund request.
            callback_url: If a refund callback for a transaction is required on a specific URL, the URL
                must be specified in this parameter.
            instant_refund: This parameter must contain the details of customer and funds need to be
                credited in a JSON format.
                {
                    "refund_mode":"2",
                    "beneficiary_full_name":"",
                    "beneficiary_account":"",
                    "beneficiary_ifsc":""
                }
        """
        for col in ['payment_id', 'refund_id', 'amount']:
            if not kwargs.get(col):
                raise KeyError(f"{col} mandatory missing in request payload ")

        payload = {}
        for key, value in PAYU_CONFIGS['refund_mapping'].items():
            if kwargs.get(value):
                payload.update({
                    key: kwargs.get(value)
                })
        payload['command'] = "cancel_refund_transaction"
        response = self.__make_request(**payload)
        return response

    def refund_status(self, *args, **kwargs):
        """
            In check_action_status API,
            you need to input this Refund ID to get the current status of the request.
            The return parameters are MIHPayID, Amount, Discount, Mode, and Status of transaction.
            refund_id
        """
        if not kwargs.get('refund_id'):
            raise KeyError(" refund_id missing from requested payload")

        kwargs['var1'] = kwargs.pop('refund_id')
        kwargs['command'] = "check_action_status"
        response = self.__make_request(**kwargs)
        return response
