## PAYWIX with Payu

In this document will give the detailed information about the payu configuration for the python based applications.

------------
### Example Project for payu

- [payu django 4.0](https://github.com/renjithsraj/paywix/blob/master/payu_django.md "payu django 3.1.6")


### Setup account with PAYU setup account with PAYU

  - Create an account with Payu
    + [Create Merchant Account](https://onboarding.payu.in/app/account/signup)
  - Copy the Merchant Key and Merchant Salt for integrating Payment gateway
    + Make sure that the mode of the transaction is `test` , when you're testing

------------

### Initial setup

```python
PAYU_CONFIG = {
    "merchant_key": "******",
    "merchant_salt": "******",
    "mode": "test",
    "success_url": "http://127.0.0.1:8000/success",
    "failure_url": "http://127.0.0.1:8000/failure"
}
```
| No  | keyname  |  description |
| ------------ | ------------ | ------------ |
|  1 |  merchant_key |   key provided from payu dashboard|
| 2  |  mercahnt_salt |  salt provided from payu dashboard |
|  3 |   mode|  transaction mode [TEST, LIVE] |
|  4 |  success_url |   where we want to redirect after the success transaction|
|  5 |   failure_url|  where we want to redirect after the failure transaction  |

### Prepare paywix integration for payu transaction

``` python
from paywix.payu import Payu

payu_config = PAYU_CONFIG
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')

# Create payu instance
payu = Payu(merchant_key, merchant_salt, surl, furl, mode)
data = {
    'amount': '10', 'firstname': 'renjith',
    'email': 'renjithsraj@gmail.com',
    'phone': '9746272610', 'productinfo': 'test',  'lastname': 'test', 'address1': 'test',
    'address2': 'test', 'city': 'test',  'state': 'test', 'country': 'test',
    'zipcode': 'tes', 'udf1': '', 'udf2': '', 'udf3': '', 'udf4': '', 'udf5': ''
}
# Make sure the transaction ID is unique
txnid = "Create your transaction id"
data.update({"txnid": txnid})
payu_data = payu.transaction(**data)

```
The payu_data will contain all the required parameters for the payu payment transaction process,  we pass the given dictionary data into the `payu_checkout.html` page, the template I'm attaching with document,

``` html
# payu_checkout.html
  <html>
  <head>
      <title>Loading...</title>
  </head>

  <body onload="document.payuForm.submit()">
      <form action={{ posted.action }} method="post" name="payuForm">
          <input type="hidden" name="key" value="{{posted.key}}" />
          <input type="hidden" name="hash_string" value="{{ posted.hash_string }}" />
          <input type="hidden" name="hash" value="{{ posted.hashh }}" />
          <input type="hidden" name="posted" value="{{ posted }}" />
          <input type="hidden" name="txnid" value="{{ posted.txnid }}" />
          <input type="hidden" name="amount" value="{{ posted.amount|default:'' }}" /></td>
          <input type="hidden" name="firstname" id="firstname" value="{{ posted.firstname|default:'' }}" /></td>
          <input type="hidden" name="email" id="email" value="{{ posted.email|default:'' }}" /></td>
          <input type="hidden" name="phone" value="{{ posted.phone|default:'' }}" /></td>
          <textarea type="hidden" name="productinfo" style="display:none;">{{ posted.productinfo|default:'' }}</textarea>
          </td>
          <input type="hidden" name="surl" value="{{ posted.surl }}" size="64" /></td>
          <input type="hidden" name="furl" value="{{ posted.furl }}" size="64" /></td>
          <input type="hidden" name="service_provider" value="{{posted.service_provider}}" size="64" />
          <input type="hidden" name="lastname" id="lastname" value="{{ posted.lastname }}" /></td>
          <input type="hidden" name="address1" value="{{ posted.address1 }}" /></td>
          <input type="hidden" name="address2" value="{{ posted.address2 }}" /></td>
          <input type="hidden" name="city" value="{{ posted.city }}" /></td>
          <input type="hidden" name="state" value="{{ posted.state }}" /></td>
          <input type="hidden" name="country" value="{{ posted.country }}" /></td>
          <input type="hidden" name="zipcode" value="{{ posted.zipcode }}" /></td>
          <input type="hidden" name="udf1" value="{{ posted.udf1 }}" /></td>
          <input type="hidden" name="udf2" value="{{ posted.udf2 }}" /></td>
          <input type="hidden" name="udf3" value="{{ posted.udf3 }}" /></td>
          <input type="hidden" name="udf4" value="{{ posted.udf4 }}" /></td>
          <input type="hidden" name="udf5" value="{{ posted.udf5 }}" /></td>
      </form>
  </body>
  </html>
```
After the transaction payu will return to the provided the urls(success|failure). in the function we have to verify the response with `verify_transaction` function. example given below.

```python
data = {k: v[0] for k, v in dict(request.POST).items()}
response = payu.verify_transaction(data)

response:
     {"return_data": {"isConsentPayment": "0", "mihpayid": "250403759", "mode": "", "status": "failure", "unmappedstatus": "userCancelled", "key": "3o6jgxhp", "txnid": "tmk f23b118be0500854f90d", "amount": "10.00", "addedon": "2020-07-27 14:00:40", "productinfo": "test", "firstname": "renjith", "lastname": "", "address1": "dsf", "address2": "fsdf", "city": "sdf", "state": "", "country": "", "zipcode": "342341", "email": "renjith", "phone": "9746272610", "udf1": "", "udf2": "", "udf3": "", "udf4": "", "udf5": "", "udf6": "", "udf7": "", "udf8": "", "udf9": "", "udf10": "", "hash": "cdb80b5e3973fb048782152aa8b5a5fd9d58915578fec92cbd55780bc36821fb90f7741a251c01724903ea7ccc3c5fa3f5b16d4aa4255c62f3d4da707d357265", "field1": "", "field2": "", "field3": "", "field4": "", "field5": "", "field6": "", "field7": "", "field8": "", "field9": "Cancelled by user", "PG_TYPE": "PAISA", "bank_ref_num": "250403759", "bankcode": "PAYUW", "error": "E000", "error_Message": "No Error", "payuMoneyId": "250403759"}, "hash_string": "67bAgZX1B3|failure|||||||||||renjith|renjith|test|10.00|tmk f23b118be0500854f90d|3o6jgxhp", "generated_hash": "cdb80b5e3973fb048782152aa8b5a5fd9d58915578fec92cbd55780bc36821fb90f7741a251c01724903ea7ccc3c5fa3f5b16d4aa4255c62f3d4da707d357265", "recived_hash": "cdb80b5e3973fb048782152aa8b5a5fd9d58915578fec92cbd55780bc36821fb90f7741a251c01724903ea7ccc3c5fa3f5b16d4aa4255c62f3d4da707d357265", "hash_verified": true}
```

### PAYU API Reference

If you want to use API services for the Payu, you have to include the `auth_header` in the `Payu(auth_header="")` class, default value is `None`,

#### Get Payment Response

This API can be used by the merchant to get the response details of the transaction(s) done using PayUmoney.

ID | PARAM | Description | type | mandatory|
---|-------|-------------|------|----------|
1 | required_data  | Mandataory Details {"ids": <merchant transaction ids>(list)}| dict | Yes
2 | optionals | optionals data `{"from_date":, "to_date":, "count":}`| dict | No

> Sample for Getpayment response function

```python
payment_Resp = payu.getPaymentResponse({"ids": ['172b0970-d073-11ea-8a7c-f0189853078a']})
```
> Response

```json
{
  "errorCode": "",
  "message": "All txnIds are valid",
  "responseCode": "",
  "result": [
    {
      "merchantTransactionId": "396132-58876806",
      "postBackParam": {
        "addedon": "2017-04-26T15:22:05.000Z",
        "additionalCharges": "6.1",
        "additional_param": "",
        "address1": "",
        "address2": "",
        "amount": "100.0",
        "amount_split": "{\"PAYU\":\"106.1\"}",
        "bank_ref_num": "1182885976",
        "bankcode": "MAST",
        "calledStatus": "false",
        "cardToken": "",
        "card_merchant_param": "",
        "card_type": "",
        "cardhash": "This field is no longer supported in postback params.",
        "cardnum": "500446XXXXXX0000",
        "city": "",
        "country": "",
        "createdOn": "1493200111000",
        "discount": "0.00",
        "email": "test@email.com",
        "encryptedPaymentId": "",
        "error": "E000",
        "error_Message": "No Error",
        "fetchAPI": "",
        "field1": "",
        "field2": "",
        "field3": "",
        "field4": "",
        "field5": "",
        "field6": "",
        "field7": "",
        "field8": "",
        "field9": "",
        "firstname": "Tom Jude",
        "hash": "9a5e632d332c11eb74f8a76ba3dcccd0548f1f26a73bc2541f85198a3cf0eb948ad8caff6b0921ae9a11aa7648c70f0a87ac29d09790ba2f1c31d48823ba9a85",
        "key": "40747T",
        "lastname": "",
        "meCode": "{\"tranportalid\":\"90000970\",\"pg_alias\":\"90000970\",\"pg_name\":\"hdfctraveltesting\",\"tranportalpwd\":\"password\"}",
        "mihpayid": "70000000688113",
        "mode": "DC",
        "name_on_card": "Tom",
        "net_amount_debit": "106.1",
        "offer_availed": "",
        "offer_failure_reason": "",
        "offer_key": "",
        "offer_type": "",
        "paisa_mecode": "",
        "paymentId": "58876806",
        "payuMoneyId": "58876806",
        "pg_TYPE": "HDFCPG",
        "pg_ref_no": "",
        "phone": "6121212232",
        "postBackParamId": "39803778",
        "postUrl": "https://test.payumoney.com/customer/dashboard/#/payment/notification/success",
        "productinfo": "productInfo",
        "state": "",
        "status": "sucess",
        "txnid": "396132-58876806",
        "udf1": "",
        "udf10": "",
        "udf2": "",
        "udf3": "",
        "udf4": "",
        "udf5": "",
        "udf6": "",
        "udf7": "",
        "udf8": "",
        "udf9": "",
        "unmappedstatus": "captured",
        "version": "",
        "zipcode": ""
      }
    }
  ],
  "status": "0"
}
```

#### Check Merchant Transaction Status

This API can be used by a merchant to reconcile/get update status of the transaction(s) with PayUmoney.


ID | PARAM | Description | type | mandatory|
---|-------|-------------|------|----------|
1 | required_data  | Mandataory Details {"ids": <merchant transaction ids>(list)}| dict | Yes

> Sample Check Merchant Transaction

```python
payment_Resp = payu.chkMerchantTxnStatus({"ids": ['172b0970-d073-11ea-8a7c-f0189853078a', '172b0970-d073-11ea-8a7c-f0189853078a']})
```
```json
{
  "errorCode": "",
  "message": "All txnIds are valid",
  "responseCode": "",
  "result": {
    "amount": "106.1",
    "merchantTransactionId": "396132-58876806",
    "paymentId": "58876806",
    "status": "Money with Payumoney"
  },
  "status": "0"
}
```

<aside class="warning"> Refund Related API only works in  lie </aside>


#### Refund Payment API
This API can be used by the merchant to initiate a partial or full refund for any successful transaction.


ID | PARAM | Description | type | mandatory|
---|-------|-------------|------|----------|
1 | required_data  | Mandataory Details {"payu_id": <transaction id from payu>, "amount": <>}| dict | Yes

> Sample Refund Payment API

```python
    refund_amount = payu.refundPayment({'payu_id': 58872009, 'amount': 5})
```
```json
{
  "errorCode": "",
  "guid": "",
  "message": "Refund Initiated",
  "result": "190651",
  "rows": "0",
  "sessionId": "",
  "status": "0"
}
```

#### Get Refund Details by Refund Id

This API returns all the refund details of a particular refund done using the Refund API or the Payumoney panel.

ID | PARAM | Description | type | mandatory|
---|-------|-------------|------|----------|
1 | required_data  | Mandataory Details {"refund_id": <response from refund api>| dict | Yes

> Sample Get Refund Details by Refund Id

```python
    rrefund_details_1 = payu.getRefundDetails({'refund_id': 190783})
```
response
```json
{
  "errorCode": "",
  "guid": "",
  "message": "Refund Details :",
  "result": {
    "PaymentId": "58876807",
    "Refund Amount": "1.0",
    "Refund Completed On": "null",
    "Refund Created On": "2017-04-26T15:59:51.000Z",
    "Refund Status": "refundinprogress",
    "RefundId": "190783",
    "Total Amount": "1.06"
  },
  "rows": "0",
  "sessionId": "",
  "status": "0"
}
```

#### Get Refund Details by Payment Id

This API returns details of all refunds for a payment done through Payumoney.


ID | PARAM | Description | type | mandatory|
---|-------|-------------|------|----------|
1 | required_data  | Mandataory Details {"payu_id": <transaction id from payu>| dict | Yes

> Sample Get Refund Details by Payment Id

```python
    rrefund_details = payu.getRefundDetailsByPayment({'payu_id': 190783})

```
response
```json
{
  "errorCode": "",
  "guid": "",
  "message": "Refund Details :",
  "result": {
    "PaymentId": "58876807",
    "Amount Left": "1266.0",
    "Refund Details Map": "[{RefundId=190783, Refund Amount=10.0, Refund Completed On=null, Refund Status=refundinprogress, Refund Created On=2017-04-26 15:59:51.0}]",
    "Total Amount": "1276.0"
  },
  "rows": "0",
  "sessionId": "",
  "status": "0"
}
```
















