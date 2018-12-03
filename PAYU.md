# PAYU PAYMENT GATEWAY

```python

project/settings.py # Add following parameters 

PAYU_MERCHANT_KEY = "mPXEdCTk" # Merchant key from payu
PAYU_KEY = "mPXEdCTk"
PAYU_SALT = "eWC5pLKLDY" # Merchant salt from payu
PAYMENT_MODE ='TEST'
PAYU_SUCCESS_URL = 'http://127.0.0.1:8000/payment/success' # success url
PAYU_FAILURE_URL = 'http://127.0.0.1:8000/payment/failure' # failure url

project/app/views.py # import paywix and do the integrations

from * import *
from paywix.payu import PAYU
import hashlib
from random import randint
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect, JsonResponse


# Import Payu from PAYWIX
payu = PAYU()

# Intiate transaction
def checkout(request):
    # Creating unique Transaction ID(change as per your need)
    hash_object = hashlib.sha256(b'randint(0,20)')
    txnid=hash_object.hexdigest()[0:20]
    # payment_data = {
	# 				'txnid': txnid,
	# 				'amount': '10',
	# 				'firstname': 'Renjith',
	# 				'email': 'renjithsraj91@gmail.com',
	# 				'phone': '9746272610',
	# 				'productinfo': 'trst',
	# 				'lastname': 's raj',
	# 				'address1': '',
	# 				'address2': 'dsadasd',
	# 				'city': 'Chennai',
	# 				'state': 'Tamilnadu',
	# 				'country': 'India',
	# 				'zipcode': '600113',
	# 				'udf1': 'dsad',
	# 				'udf2': 'dsfsf',
	# 				'udf3': 'sdffsdf',
	# 				'udf4': 'dfsfds',
	# 				'udf5': 'fsdfsdf'
	# 				}

	# You can use any of the dict items for configure payu
    # The above payment_data contains mandatory and optional parameters
    # The below payment_data contains on the mandatory items

	payment_data = {
					'txnid': txnid,
					'amount': '10',
					'firstname': 'Renjith',
					'email': 'renjithsraj91@gmail.com',
					'phone': '9746272610',
					'productinfo': 'trst'
					}
	# Once you make your Dict, Initiate with PAYU
	payu_data = payu.initate_transaction(payment_data)

	# The payu_data contains the input data for the pay payment data
	return render(request, 'payment_form.html',{"posted":payu_data})

# templates/payment_form.html

for sample payment_form you can find it from the templates folder change the templates styles 
as per your needs, in this templates you can make some fields hidden (success url, failure url and etc) please consider, provided templates is only for demo purpose 


# Success URL
@csrf_protect
@csrf_exempt
def payment_success(request):
   # Payu will return response success data with hash value 
   # Need to verify the data with payu check_hash

	payu_success_data = payu.check_hash(dict(request.POST))
	# The payu_success_data return the response data from the payu 
	# The hash value is correct or not, with this validation we can find out the 
	# whether the response is correct or not

	# Here I just dump the response, Here you have to do your calculations with the data
	return JsonResponse(payu_success_data)

# Failure URL
@csrf_protect
@csrf_exempt
def payment_failure(request):
	# Payu will return response success data with hash value 
   # Need to verify the data with payu check_hash


	payu_failure_data = payu.check_hash(dict(request.POST))
	# The payu_failure_data return the response data from the payu 
	# The hash value is correct or not, with this validation we can find out the 
	# whether the response is correct or not

	# Here I just dump the response, Here you have to do your calculations with the data
	return JsonResponse(payu_failure_data)

```