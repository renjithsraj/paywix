# Paywix with Payu

### Setup Payu payment gateway
  - Create an account with Payu
    + [Create Merchant Account](https://www.payumoney.com/merchant-dashboard/)
  - Copy the Merchant Key and Merchant Salt for integrating Payment gateway
    + Make sure that the mode of the transaction is `test` , when you're testing
  - Create a config file like follow.
   
> Make config file like this in your project root

```json
  PAYU_CONFIG = {
        "merchant_key": "3o6jgxhp",
        "merchant_salt": "67bAgZX1B3",
        "mode": "test",
  }
```

# Payu Pawix with Django


### Configure Django Projecct Settings(project/setting.py)

> install `paywix` on INSTALLED_APPS 


```python

project/setting.py

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'checkout.apps.CheckoutConfig',
    'paywix',
]
```
> Make a config file with payu details on settings.py

``` python

# PAYU Mandatory Config details
# No specific schema, you can use any other methods

PAYU_CONFIG = {
    "merchant_key": "******",
    "merchant_salt": "******",
    "mode": "test",
    "success_url": "http://127.0.0.1:8000/success",
    "failure_url": "http://127.0.0.1:8000/failure"
}
```

### Configure urls
  - Create `success` and `failure` url in `checkout` app (change it with your needs)

### Configure template

Create a template file called `payu_checkout.html` is template is used get the data from checkout views(functionality) and redirect to `payu` payment gateway. 

<aside class="warning">Don't change the structure for the HTML</aside>

> Configure Template [Make sure the template should be given format

``` html
templates/payu_checkout.html
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

### Configure Payu in views(checkout)

The given views is a example intreation, you have to make changes as per your needs, consider this as sample view. when the customer click the checkout function, redirect to given function then we have to make the `data` as per the given format, make sure you have included all the mandatory params.

<aside class="warning">Please ensure that all the data stored in appropriate tables</aside>

> Consider the this as sample views

``` python
checkout/views.py

from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Import Payu from Paywix
from paywix.payu import Payu

payu_config = settings.PAYU_CONFIG
merchant_key = payu_config.get('merchant_key')
merchant_salt = payu_config.get('merchant_salt')
surl = payu_config.get('success_url')
furl = payu_config.get('failure_url')
mode = payu_config.get('mode')

# Create Payu Object for making transaction
# The given arguments are mandatory
payu = Payu(merchant_key, merchant_salt, surl, furl, mode)


# Payu checkout page
@csrf_exempt
@login_required
def payu_checkout(request):
    if request.method == 'POST':
        # Making Checkout form into dictionary
        data = {k: v[0] for k, v in dict(request.POST).items()}
        data.pop('csrfmiddlewaretoken')
        # The dictionary data  should be contains following details
        # data = { 'amount': '10', 
        #     'firstname': 'renjith', 
        #     'email': 'renjithsraj@gmail.com',
        #     'phone': '9746272610', 'productinfo': 'test', 
        #     'lastname': 'test', 'address1': 'test', 
        #     'address2': 'test', 'city': 'test', 
        #     'state': 'test', 'country': 'test', 
        #     'zipcode': 'tes', 'udf1': '', 
        #     'udf2': '', 'udf3': '', 'udf4': '', 'udf5': ''
        # }

        # No Transactio ID's, Create new with paywix, it's not mandatory
        # Create your own
        # Create transaction Id with payu and verify with table it's not existed
        txnid = "Create your transaction id"
        data.update({"txnid": txnid})
        payu_data = payu.transaction(**data)
        return render(request, 'payu_checkout.html', {"posted": payu_data})
```

### Configure Success & Failure urls

URL | Description
--------- | -----------
success | To handle successfull transactions
failure | To handle un-successfull transactions

#### Success Views

<aside class="warning">Please ensure that all the data stored in appropriate tables</aside>

> Consider the this as sample views

``` python
# Payu success return page
@csrf_exempt
def payu_success(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    return JsonResponse(response)
```

<aside class="warning">Please ensure that all the data stored in appropriate tables</aside>

> Consider the this as sample views

#### Failure Views

``` python
# Payu failure page
@csrf_exempt
def payu_failure(request):
    data = {k: v[0] for k, v in dict(request.POST).items()}
    response = payu.verify_transaction(data)
    return JsonResponse(response)
```


### Payu include follows

+ `Payu()` --> Initialize with following arguments

  + `merchant_key`  - Mercahnt Key from Payu merchant Dashboard
  + `merchant_salt` - Mercahnt Salt from Payu merchant Dashboard
  + `surl`          - After successfull transaction where to redirect
  + `furl` - After failured transactoin where to redirect
  + `mode` - Transaction mode(test/live)

+ `payu.generate_txnid()` -> Not mandatory
  + This methods is used to generate transaction id's, make sure that the returnd id always unique, so you have to validate with your transaction table(Important)
  + This is not manadatory function, if you need you can use it.
  + `prefix` -> While generate the transaction id's if you required some thing like `tmk_` in the prefix of txnid, then you can include this arg
  + `limit`-> length of the transaction id's -> default - 20

+ `payu.transaction(**data)`

  The method will processed data for making transaction, we have to pass data as kwargs. Once the function processd the data, will contains the hash values, hashstring etc. you can logging once you start digging.

> sample for `payu.transaction(**data)`

```python
   data = {
     'amount': '10', 
     'firstname': 'renjith', 
     'email': 'renjithsraj@gmail.com',
     'phone': '9746272610', 'productinfo': 'test', 
     'lastname': 'test', 'address1': 'test', 
     'address2': 'test', 'city': 'test', 
     'state': 'test', 'country': 'test', 
     'zipcode': 'tes', 'udf1': '', 
     'udf2': '', 'udf3': '', 'udf4': '', 'udf5': ''
  }
  data.update({'txnid': "xyz"})
  posted_data = payu.transaction(**data)
```

+ `payu.verify_transaction()`
  + This function is used to verify the transaction(verify the response data from payu)
  + The function will create the hash value with transaction data and verify with payu response hash value, if it's True, Then transaction is successfully done.

> sample for `payu.verify_transaction(data)`

```python
  data = {k: v[0] for k, v in dict(request.POST).items()}
  response = payu.verify_transaction(data)
```

> response for `payu.verify_transaction(data)`

``` javascript
     {"return_data": {"isConsentPayment": "0", "mihpayid": "250403759", "mode": "", "status": "failure", "unmappedstatus": "userCancelled", "key": "3o6jgxhp", "txnid": "tmk f23b118be0500854f90d", "amount": "10.00", "addedon": "2020-07-27 14:00:40", "productinfo": "test", "firstname": "renjith", "lastname": "", "address1": "dsf", "address2": "fsdf", "city": "sdf", "state": "", "country": "", "zipcode": "342341", "email": "renjith", "phone": "9746272610", "udf1": "", "udf2": "", "udf3": "", "udf4": "", "udf5": "", "udf6": "", "udf7": "", "udf8": "", "udf9": "", "udf10": "", "hash": "cdb80b5e3973fb048782152aa8b5a5fd9d58915578fec92cbd55780bc36821fb90f7741a251c01724903ea7ccc3c5fa3f5b16d4aa4255c62f3d4da707d357265", "field1": "", "field2": "", "field3": "", "field4": "", "field5": "", "field6": "", "field7": "", "field8": "", "field9": "Cancelled by user", "PG_TYPE": "PAISA", "bank_ref_num": "250403759", "bankcode": "PAYUW", "error": "E000", "error_Message": "No Error", "payuMoneyId": "250403759"}, "hash_string": "67bAgZX1B3|failure|||||||||||renjith|renjith|test|10.00|tmk f23b118be0500854f90d|3o6jgxhp", "generated_hash": "cdb80b5e3973fb048782152aa8b5a5fd9d58915578fec92cbd55780bc36821fb90f7741a251c01724903ea7ccc3c5fa3f5b16d4aa4255c62f3d4da707d357265", "recived_hash": "cdb80b5e3973fb048782152aa8b5a5fd9d58915578fec92cbd55780bc36821fb90f7741a251c01724903ea7ccc3c5fa3f5b16d4aa4255c62f3d4da707d357265", "hash_verified": true}

```

### Note

+ Paywix is not storing any data into Table
+ Make sure the Transaction Data is stored into Table before making transaction.
+ When the transaction got sucees/faild, make sure that the data also stored in somewhere in db



