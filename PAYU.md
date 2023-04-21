## PLEASE USE YOUR CREDENTIALS WHILE MAKING TRANSACTIONS, SOME PEOPLE ARE USING MY CREDENTIALS AND DETAILS, NOW I"M FEELING I HAVE DID A BIG MISTAKE


## PAYWIX with Payu



In this document will give the detailed information about the payu configuration for the python based applications.



------------
### Example Project for payu with paywix

- [payu django 4.0](https://github.com/renjithsraj/paywix_ecommerce)


### Setup account with PAYU setup account with PAYU

  - Create an account with Payu
    + [Create Merchant Account](https://onboarding.payu.in/app/account/signup)
  - Copy the Merchant Key and Merchant Salt for integrating Payment gateway
    + Make sure that the mode of the transaction is `test` , when you're testing

------------

### Initial setup

```python
MERCHANT_KEY = "gtKFFx"
MERCHANT_SALT = "4R38IvwiV57FwVpsgOvTXBdLE4tHUXFW"
RESPONSE_URL_SUCCESS = "http://127.0.0.1:8000/payment_response_handler/"
RESPONSE_URL_FAILURE = "http://127.0.0.1:8000/payment_response_handler/"

```
| No  | keyname  |  description |
| ------------ | ------------ | ------------ |
|  1 |  merchant_key |   key provided from payu dashboard|
| 2  |  mercahnt_salt |  salt provided from payu dashboard |
|  3 |   mode|  transaction mode [test, live] |
|  4 |  RESPONSE_URL_SUCCESS |   where we want to redirect after the success transaction|
|  5 |   RESPONSE_URL_FAILURE|  where we want to redirect after the failure transaction  |

## Prepare paywix integration for payu transaction

``` python
from paywix.payu import Payu

# Create payu instance
payu = Payu(merchant_key, merchant_salt, surl, furl, mode)

merchant_key = settings.MERCHANT_KEY
merchant_salt = settings.MERCHANT_SALT
payu = Payu(merchant_key, merchant_salt, "Test")
```
## Required Parameters Details for Transaction
| No  | keyname  |  description | Mandatory
| ------------ | ------------ | ------------ | ------------ |
|  1 |  amount |   Amount | True |
| 2  |  firstname |  Customer firstname | True|
|  3 |   email |  Customer Email | True |
|  4 |  phone |  Customer Phone Number| True |
|  5 |   txnid|  Unique Transaction id  | True |
| 6 | furl | Failure Redirect URL | True |
| 7| surl| Success Redirect URL | True |

```
payload = {
        "amount": "230",
        "firstname": "Renjith",
        "email": "888888@hmil.com",
        "phone": "88888888888",
        "lastname": "s raj",
        "productinfo": "ORDER FOR E_CART",
        "txnid": "OR_123_45678_123",
        "furl": RESPONSE_URL_FAILURE,
        "surl": RESPONSE_URL_SUCCESS
    }

response = payu.transaction(**payload)  #transaction required keyword arguments
```

The `transaction` method will returns response for initiate transaction.
#### Response for `transaction`

``` json
{
  'amount': '749.99',
  'firstname': 'Renjith',
  'email': '',
  'phone': '',
  'lastname': 'S Raj',
  'productinfo': '21_fe68a0676df144a688fb287b3c4835fe',
  'txnid': '21_fe68a0676df144a688fb287b3c4835fe',
  'furl': 'http://127.0.0.1:8000/payment_response_handler/',
  'surl': 'http://127.0.0.1:8000/payment_response_handler/',
  'key': 'gtKFFx',
  'hash': 'a76f15a7a05ec50069192ccece89a7b76344a85fdb8b9b5dff9b82b47e2c5167e7104a4a7cfb8dea961bd97be68c2e5acd19b8fa85dd5676becb339516d8c12a',
  'action': 'https://test.payu.in/_payment'
}
```
#### `transaction` response in HTML Format

To get the html response, use `make_html` method with response from `transaction`

``` python
data = "Response from `transaction` "
html = payu.make_html(data) ## required paramter in dict format
```

#### Response `make_html` 
We can use below html in httpresponse, so the system will redirect to payu payment gateway
page.

``` html
<html>
   <body>
      <formaction='https://test.payu.in/_payment'method='post'id='payuform'>
      <input type="hidden"name="key"value=""/>
      <input type="hidden"name="txnid"value=""/>
      <input type="hidden"name="productinfo"value=""/>
      <input type="hidden"name="amount"value=""/>
      <input type="hidden"name="email"value=""/>
      <input type="hidden"name="firstname"value="Renjith"/>
      <input type="hidden"name="lastname"value="SRaj"/>
      <input type="hidden"name="surl"value="http://127.0.0.1:8000/success/"/>
      <input type="hidden"name="furl"value="http://127.0.0.1:8000/failure/"/>
      <input type="hidden"name="phone"value=""/>
      <input type="hidden"name="hash"value="a76f15a7a05ec50069192ccece89a7b76344a85fdb8b9b5dff9b82b47e2c5167e7104a4a7cfb8dea961bd97be68c2e5acd19b8fa85dd5676becb339516d8c12a"/></form><script>window.onload=function(){
         document.forms[
           'payuform'
         ].submit()
         }
      </script>
   </body>
</html>
```

## Verify Payment Response from PAYU

PayU will post the transaction details to the specified success URL (sURL) or failure URL (fURL) after the transaction has been processed. These URLs are specified during the transaction initialization process and are used to redirect the customer to the appropriate page on the merchant's website, depending on the outcome of the transaction.


``` json
{
  'mihpayid': '403993715528233750',
  'mode': 'CC',
  'status': 'success',
  'unmappedstatus': 'captured',
  'key': 'gtKFFx',
  'txnid': '22_0b62608a093c428887d996df967c6622',
  'amount': '179.00',
  'cardCategory': 'domestic',
  'discount': '0.00',
  'net_amount_debit': '179',
  'addedon': '2023-02-02 10:08:57',
  'productinfo': '22_0b62608a093c428887d996df967c6622',
  'firstname': 'renjith',
  'lastname': 's raj',
  'address1': '',
  'address2': '',
  'city': '',
  'state': '',
  'country': '',
  'zipcode': '',
  'email': '',
  'phone': '',
  'udf1': '',
  'udf2': '',
  'udf3': '',
  'udf4': '',
  'udf5': '',
  'udf6': '',
  'udf7': '',
  'udf8': '',
  'udf9': '',
  'udf10': '',
  'hash': 'fb0e269ca7f377d83efb31144b6e37336e00e613cc44ce56fab2535c1dcbcd4e4fda46a9ba06599fb1e651001c994b88d6cf08825526f67dc709bd022fdfa621',
  'field1': '',
  'field2': '',
  'field3': '',
  'field4': '',
  'field5': '',
  'field6': '',
  'field7': '',
  'field8': '',
  'field9': 'Transaction Completed Successfully',
  'payment_source': 'payu',
  'PG_TYPE': '',
  'bank_ref_num': 'ae1b30b6-76f5-41e2-aa39-8c41985c003f',
  'bankcode': 'CC',
  'error': 'E000',
  'error_Message': 'No Error',
  'cardnum': 'XXXXXXXXXXXX2346',
  'cardhash': 'This field is no longer supported in postback params.',
  'issuing_bank': 'UNKNOWN',
  'card_type': 'UNKNOWN'
}
```

## Verify the payment response from payu
``` python
response = payu.check_transaction(**data)
```
#### Verify `response` from `check_transaction`

```json
{
  'hash_response': {
    'hash_string': '4R38IvwiV57FwVpsgOvTXBdLE4tHUXFW|success|||||||||||renjithsraj@live.com|renjith|22_0b62608a093c428887d996df967c6622|179.00|22_0b62608a093c428887d996df967c6622|gtKFFx',
    'hash_value': 'fb0e269ca7f377d83efb31144b6e37336e00e613cc44ce56fab2535c1dcbcd4e4fda46a9ba06599fb1e651001c994b88d6cf08825526f67dc709bd022fdfa621',
    'is_hash_verified': True
  },
  'all_response': { ## same response from payu ## },
  'payment_response': {
    'mihpayid': '403993715528233750',
    'status': 'success',
    'error': 'NO_ERROR',
    'mode': 'CC',
    'bank_code': 'Credit Card',
    'payment_source': 'payu',
    'transaction_msg': 'Transaction Completed Successfully',
    'transaction_id': '22_0b62608a093c428887d996df967c6622'
  }
}
```
ID | response key | Description | type |
---|-------|-------------|------|
1 | hash_response | How Hash value calcuation in paywix | dict
2 | all_response | Actual payment response from payu | dict
3| payment_response | Important things to remember for future use | dict


## Verify Payment with Payment ID
This API gives you the status of the transaction.

transaction_id => Unique Transaction id generated while initializing transaction.
``` python
verify_payment_data = {
    'transaction_id': ['20_95e00e4941c94ac5a124989b8c5a9dba']
}
verify_payment_resp = payu.verify_payment(**verify_payment_data)
```
### Verifyment `verify_payment` response
``` json
{
        'status': 1,
        'msg': '1 out of 1 Transactions Fetched Successfully',
        'transaction_details': {
            '20_95e00e4941c94ac5a124989b8c5a9dba': {
                'mihpayid': '403993715528207372',
                'request_id': '',
                'bank_ref_num': 'da5780ef-c69b-44df-b625-bdae45c1a358',
                'amt': '1074.00',
                'transaction_amount': '1074.00',
                'txnid': '20_95e00e4941c94ac5a124989b8c5a9dba',
                'additional_charges': '0.00',
                'productinfo': '20_95e00e4941c94ac5a124989b8c5a9dba',
                'firstname': 'renjith',
                'bankcode': 'CC',
                'udf1': None,
                'udf3': None,
                'udf4': None,
                'udf5': None,
                'field2': None,
                'field9': 'Transaction Completed Successfully',
                'error_code': 'E000',
                'addedon': '2023-01-29 12:13:10',
                'payment_source': 'payu',
                'card_type': 'MAST',
                'error_Message': 'NO ERROR',
                'net_amount_debit': 1074,
                'disc': '0.00',
                'mode': 'CC',
                'PG_TYPE': 'CC-PG',
                'card_no': 'XXXXXXXXXXXX2346',
                'name_on_card': None,
                'udf2': None,
                'field5': None,
                'field7': None,
                'status': 'success',
                'unmappedstatus': 'captured',
                'Merchant_UTR': None,
                'Settled_At': '0000-00-00 00:00:00'
            }
        }
    }
```

## check_payment 
This API gives you the status of the transaction similar to verify_payment API. The only difference is that the input parameter in this is payment_id from payu.

`payment_id => PayUID (MihpayID) generated at PayU’s`

```python
check_payment_data = {
    'payment_id': "403993715528207372"
}
check_payment_resp = payu.check_payment(**check_payment_data)
```
### check_payment response

``` json
{
  'status': 1,
  'msg': 'Transaction Fetched Successfully',
  'transaction_details': {
    'request_id': '135006457',
    'bank_ref_num': 'da5780ef-c69b-44df-b625-bdae45c1a358',
    'net_amount': None,
    'mihpayid': 403993715528207372,
    'amt': '1074.00',
    'disc': '0.00',
    'mode': 'CC',
    'txnid': '20_95e00e4941c94ac5a124989b8c5a9dba',
    'amount': '1074.00',
    'amount_paid': '1074.00',
    'discount': '0.00',
    'additional_charges': '0.00',
    'udf1': None,
    'udf2': None,
    'udf3': None,
    'udf4': None,
    'udf5': None,
    'field1': None,
    'field2': None,
    'field3': None,
    'field4': None,
    'field5': None,
    'field6': None,
    'field7': None,
    'field8': None,
    'field9': 'Transaction Completed Successfully',
    'addedon': '2023-01-29 12:13:10',
    'status': 'success',
    'net_amount_debit': 1074,
    'unmappedstatus': 'captured',
    'firstname': 'renjith',
    'bankcode': 'CC',
    'productinfo': '20_95e00e4941c94ac5a124989b8c5a9dba',
    'payment_source': 'payu',
    'name_on_card': None,
    'card_no': 'XXXXXXXXXXXX2346',
    'PG_TYPE': 'Test PG',
    'Merchant_UTR': None,
    'Settled_At': None
  }
}
```

## get_wsonline_response
This API is used to get the transaction response sent on surl/furl.

`transaction_id => unique id generated at the time of payment initialization`

``` python
get_wsonline_data = {
    'transaction_id': '20_95e00e4941c94ac5a124989b8c5a9dba'
}
get_wsonline_resp = payu.get_wsonline_response()(**get_wsonline_data)
```
### `get_wsonline_resp` response

``` json
{
  'status': 1,
  'msg': '12 out of 32 Transactions Fetched Successfully',
  'transaction_details': {
    '5': {
      'mihpayid': '403993715510372248',
      'request_id': '',
      'bank_ref_num': '4747839251343141',
      'amt': '0.00',
      'transaction_amount': '458.00',
      'txnid': '5',
      'additional_charges': '0.00',
      'productinfo': '10092-Oriflame Tender Care Cherry Protecting Balm-22879  ',
      'firstname': 'Rajesh Goel',
      'bankcode': 'CC',
      'udf1': '5',
      'udf3': None,
      'udf4': None,
      'udf5': None,
      'field2': '999999',
      'field9': 'SUCCESS',
      'error_code': 'E000',
      'addedon': '2014-11-10 13:24:12',
      'payment_source': 'payu',
      'card_type': 'UNKNOWN',
      'error_Message': 'NO ERROR',
      'net_amount_debit': 458,
      'disc': '0.00',
      'mode': 'CC',
      'PG_TYPE': 'CC-PG',
      'card_no': '512345XXXXXX2346',
      'name_on_card': 'Amar',
      'udf2': '1031',
      'field5': None,
      'field7': '',
      'status': 'success',
      'unmappedstatus': 'captured',
      'Merchant_UTR': None,
      'Settled_At': '0000-00-00 00:00:00'
    }
}
```

## get_transaction_details 

This Method is used to extract the transaction details between two given time periods.
`date_from => start_date`
`date_to => end_date`

> date_from and date_to should 7 days interval


``` python
get_transction_details_payload = {
    'date_from': "2023-01-29",
    'date_to': "2023-01-30"
}
transaction_resp = payu.get_transaction_details(**get_transction_details_payload)
```
### `transaction_resp` response for `get_transaction_details`

``` json
{
    'status': 1,
    'msg': 'Transaction Fetched Successfully',
    'Transaction_details': [
        {
            'id': '403993715528206610',
            'status': 'failed',
            'key': 'gtKFFx',
            'merchantname': 'PayU Test Account',
            'txnid': 'TRXN20230129001212661',
            'firstname': 'qwer',
            'lastname': None,
            'addedon': '2023-01-29 00:12:17',
            'bank_name': 'Test Credit Card',
            'payment_gateway': 'Test PG',
            'phone': '',
            'email': 'test1@tester.com',
            'transaction_fee': '136.50',
            'amount': '136.50',
            'discount': '0.00',
            'additional_charges': '0.00',
            'productinfo': ' 003 ',
            'error_code': 'E500',
            'bank_ref_no': None,
            'ibibo_code': 'CC',
            'mode': 'CC',
            'ip': '122.162.146.171',
            'card_no': 'XXXXXXXXXXXX1111',
            'cardtype': 'domestic',
            'offer_key': '',
            'field0': None,
            'field1': None,
            'field2': None,
            'field3': None,
            'field4': None,
            'field5': None,
            'field6': None,
            'field7': None,
            'field8': None,
            'field9': 'invalid input',
            'udf1': None,
            'udf2': None,
            'udf3': None,
            'udf4': None,
            'udf5': None,
            'address2': '',
            'city': '',
            'zipcode': '',
            'pg_mid': None,
            'issuing_bank': '',
            'offer_type': None,
            'failure_reason': None,
            'mer_service_fee': None,
            'mer_service_tax': None
        }
    ]
}
```

## get_transaction_info 
This Method works exactly the same way as get_Transaction_Details API. The only enhancement is that this API can take input as the exact time in terms of minutes and seconds also, `date_time_from` and `date_time_to` are starting & end dates of transactions with time, respectively.

`date_time_from => datetime from`
`date_time_to => datetime to`

``` python
get_transaction_payload = {
    'date_time_from': "2023-01-29 16:00:00",
    'date_time_to': "2023-01-29 18:00:00"
}
get_transaction_resp = payu.get_transaction_info(**get_transaction_payload)
```

###  response for `get_transaction_info`

``` json
{
    'status': 1,
    'msg': 'Transaction Fetched Successfully',
    'Transaction_details': [
        {
            'id': '403993715528207724',
            'action': 'failed',
            'status': None,
            'issuing_bank': None,
            'transaction_fee': '1.00',
            'key': 'gtKFFx',
            'merchantname': 'PayU Test Account',
            'txnid': '232c9852ab9b6bb8ceb0',
            'firstname': 'BL Mandawaliya',
            'lastname': None,
            'addedon': '2023-01-29 16:28:19',
            'bank_name': 'Generic Intent',
            'payment_gateway': 'AXISU',
            'phone': '9009009001',
            'email': 'blmindore1@gmail.com',
            'amount': '1.00',
            'discount': '0.00',
            'additional_charges': '0.00',
            'productinfo': 'Ok Recharge Load Wallet Money Rs.1.0',
            'error_code': 'E4197',
            'bank_ref_no': None,
            'ibibo_code': 'INTENT',
            'mode': 'UPI',
            'ip': '202.148.59.59',
            'card_no': None,
            'cardtype': None,
            'offer_key': '',
            'field0': None,
            'field1': None,
            'field2': None,
            'field3': None,
            'field4': None,
            'field5': None,
            'field6': None,
            'field7': 'TRANSACTION ID IS NOT PRESENT|U48',
            'field8': None,
            'field9': 'U48|TRANSACTION ID IS NOT PRESENT|Completed Using Verify API',
            'udf1': '',
            'udf2': '',
            'udf3': '',
            'udf4': '',
            'udf5': '',
            'address2': '',
            'city': '',
            'zipcode': '',
            'pg_mid': None,
            'offer_type': None,
            'failure_reason': None,
            'mer_service_fee': None,
            'mer_service_tax': None
        }]
    }
```

## refund
This method provides to make refund for the transaction

`payment_id`: This parameter must contain the Payu ID (mihpayid) of the transaction.
`refund_id`: This parameter must contain the Token ID (unique token from the merchant) for the refund request.
`callback_url`: If a refund callback for a transaction is required on a specific URL, the URL must be specified in this parameter.
`instant_refund`: This parameter must contain the details of customer and funds need to be
    credited in a JSON format.
    ``` json 
    {
        "refund_mode":"2",
        "beneficiary_full_name":"",
        "beneficiary_account":"",
        "beneficiary_ifsc":""
    }
    ```
Mandatory parameters

`payment_id`
`refund_id`
`amount`

``` python
    payload = {
        'payment_id': "403993715528207372",
        "refund_id": "12334qwe45",
        "amount": "100.0"
    }
    refund_resp = payu.refund(**payload)
```

### Response for `refund` 

``` json
{
    'status': 1, 
    'msg': 'Refund Request Queued', 
    'request_id': '135018119', 
    'bank_ref_num': None, 
    'mihpayid': 403993715528207372, 
    'error_code': 102
}
```

# refund_status
This method used to check the status of the refund or cancel requests.

`refund_id => Unique ID generated for making refund transaction ` 

``` python
payload = {
        "refund_id": "12334qwe45"
    }
refund_status = payu.refund_status(**payload)

```

### Response for `refund_status`

``` json
{
    'status': 0, 
    'msg': '0 out of 1 Transactions Fetched Successfully',
    'transaction_details': {
        '12334qwe45': 'No action status found'
    }
}
```
