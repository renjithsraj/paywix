# PAYTM PAYMENT GATEWAY Config

The given package is not storing any data into db, so please make sure the requested data and response data is stored 
in your database.

### Prerequisites
To Integrate PayUmoney Bolt Checkout, you must :
* [Signup](https://dashboard.paytm.com/) with PayTM as the merchant
* Get the merchant_key and merchant_id, which are available on your merchant [dashboard](https://dashboard.paytm.com/next/apikeys)

## Config PAYTM with Django project


### projects/settings.py

    ```python
    # project/project/settings.py

        INSTALLED_APPS = [
            'django.contrib.admin',
            # Register Paywix Here
            'paywix.apps.PaywixConfig'
        ]
        
        PAYTM_CONFIG = {
                "merchant_key": "*****************",
                "merchant_id": "******************",
                "callback_url": "http://127.0.0.1:8000/paytm/response",
                "mode": "TEST/LIVE",
                "website": "WEBSTAGING",
         }

    ```

### Config in Checkout view
 - Create a dict with data with your cart data and user data
 - Make sure the following data are included in the dict.
 - Please consider below checkout snippetts
 
    ``` python
    # project/checkout/views.py

        from paywix.paytm import PayTm
        paytm = PayTm()

        def paytm_checkout(request):
            amount = 10
            if amount:
                order_id = paytm.id_generater() # Change with unique id if you need.
                data_dict = {
                    'ORDER_ID': order_id,
                    'TXN_AMOUNT': amount,
                    'CUST_ID': "renjithsraj@live.com",
                }
                param_dict = paytm.initiate_transaction(data_dict)
                print ("before request", param_dict)
                return render(request, "paytm_checkout.html", {'paytmdict': param_dict})
    ```


### Verify Given Payment response[ verify hash value]
``` python

    from django.views.decorators.csrf import csrf_exempt
    # Payu response return page
    
    @csrf_exempt
    def paytm_response(request):
        print("paytm response")
        data = dict(zip(request.POST.keys(), request.POST.values()))
        response = paytm.verify_hash(data)
        return JsonResponse(response)

```

## Make sure
* Included the call back url in the settings.py
* It should be included your checkout views
    ``` python
    # checkout views
    param_dict = paytm.initiate_transaction(data_dict)
    return render(request, "paytm_checkout.html", {'paytmdict': param_dict})
   ```
* Make sure you have added `csrf_exampt` in the callback view
