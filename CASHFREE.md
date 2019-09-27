# CASHFREE PAYMENT GATEWAY Config

The given package is not storing any data into db, so please make sure the requested data and response data is stored in your database.

### Prerequisites

To Integrate Cashfree Payment gateway, you must :

- [Signup](https://merchant.cashfree.com/merchant/login) with Cashfree as the merchant
- Switch to test first
- Get the App ID and Secret Key, which are available on your merchant [dashboard](https://test.cashfree.com/merchant/pg#api-key)


### Config Cashfree payment gateway Django Project

------

```python
# project/project/settings.py

    INSTALLED_APPS = [
        'django.contrib.admin',
        # Register Paywix Here
        'paywix.apps.PaywixConfig'
    ]
    # Manadatory Config details
    CASHFREE_CONFIG = {
    	"app_id": "*************************************",
    	"secret_key": "*********************************",
    	"return_url": "*********************************",
        "notify_url": "*********************************", #OPTIONAL
    	"currency": "INR",
    	"mode": "TEST" #TEST/LIVE
	}
```


### Config in Checkout view

- Create a dict with data with your cart data and user data
- Make sure the following data are included in the dict format
- Please consider below checkout snippets

```python
from paywix.cashfree import Cashfree
cashfree = Cashfree()

#Checkout data
def cashfree_checkout(request):
    data = {}
    data.update({'order_id': cashfree.generate_txnid()})
    # Make sure that the details are stored in the db
    # data = dict(zip(request.POST.keys(), request.POST.values()))
    # data.pop('csrfmiddlewaretoken')
    # Make sure the data stored in db
    data = {
        'amount': '10',
        'order_id': '19cf379e-12ca-4f19-85fa-0b39060afb5f',
        'name': 'renjith', 
        'email': 'renjithsraj@live.com', 
        'phone': '9746272610', 
        'note': 'test'
    }
    # Important data you should include this
    pgdata = cashfree.initiate_transaction(data)
    return render(request, 'cashfree_checkout.html', {'postData': pgdata})
    
```


### Verify Given Payment response[ verify hash value]

```python
@csrf_exempt
def cashfree_response_return(request):
    # Response data in request.POST, 
    # Make sure the data stored in database
    data = dict(zip(request.POST.keys(), request.POST.values()))
    response = cashfree.verify_hash(data)
    # Data stored in db
    return JsonResponse(response)
```


## Make sure

- Included the **return_url** in the settings.py

- **notify_url** is optional [ default  **return_url**  will assign ]

- It should be included your checkout views

  ```
  # checkout views
  # Important data you should include this
  pgdata = cashfree.initiate_transaction(data)
  return render(request, 'cashfree_checkout.html', {'postData': pgdata})
  ```

- Make sure you have added `csrf_exampt` in the response_view & notify_view

