# Payu Gateway Integration
In this detail we are going to see how to implement payu payment gateway in django application with ```paypy``` package.
### How to install
Install ```paywix``` in your virtualenv using ```pip``` command.
```
	pip install paywix
```
### Payu payment gateway integration in django.

step 1 :

Add in your ``` INSTALLED_APPS ```

	
		INSTALLED_APPS = [
			'-------------',
		   	 'paypy',
		]
	

Step 2 :
Please add following  basic information about PAYU in ```settings.py```

	PAYU_KEY =  "*******" 
	PAYU_SALT =  "******"
	PAYU_SUCCESS_URL =  "add complete success redirect url"
	PAYU_FAILURE_URL = " add complete failure redirect url"
	PAYU_MODE =  "LIVE|TEST"

Step 3: 
import  ```payu``` function from paypy  into django views.py( I mean that checkout function).  please do follows

	from django.shortcuts import render
	
	## PAYU from PAYWIX
	from paywix import PayMentManager
    pm = PayMentManager()
	
	# Payu transaction views
	def payu_checkout(request):
	    # all the fields mandatory, this dict values will use to create hash value, hash string and post data	
	    data = {
		    "txnid":"123456789122212",
		    "amount": 100.00,
		    "productinfo":"TEST PRODUCT",
		    "firstname":"Renjith",
		    "email":"renjithsraj@live.com",
		    "phone":"9746272610"
		}
		# Make sure the data is in dict format and all the fields mandatory
	    response_data = pm.payu_transaction(data) # Please read the this
	    # if you print the response_data here , you can see it will be dict format data.
	    #
	    return render (request, 'payu.html', response_data
	
	NOTE: Please read this before integrate.
	The response_data contain following details. 
	{'MERCHANT_KEY': '3o6jgxhp',
	 'action': 'https://sandboxsecure.payu.in/_payment',
	 'hash_string': '3o6jgxhp|123456789122212|100.0|TEST PRODUCT|Renjith|renjithsraj@live.com|||||||||||67bAgZX1B3',
	 'hashh': 'b2cf76954c390a4aa318fb1b3c918a3a9304fb18c7f7d3314ce5539dca6ee42187493a0f8b87f07aa2e5bab2ffd6a161b62c66d0897b58efc94e0ae32bfed21a',
	 'posted': {'amount': '100.0',
	  'email': 'renjithsraj@live.com',
	  'firstname': 'Renjith',
	  'furl': '/',
	  'key': '3o6jgxhp',
	  'phone': '9746272610',
	  'productinfo': 'TEST PRODUCT',
	  'surl': '/',
	  'txnid': '123456789122212'},
	 'service_provider': 'payu_paisa',
	 'txnid': '123456789122212'}
	 
	 you can use this data for server side integration with various type of platforms like mobile,web and etc. Here I'm going to show you how to use this in out checkout option.
	 
payu.html 
```
		<html>
		  <head onload="submitPayuForm()">
		  <script type="text/javascript">
		    var hash = "{{ hashh }}";
		    function submitPayuForm() {
		      if(hash =='') {
			return;
		      }
		      var payuForm = document.forms.payuForm;
		      payuForm.submit();
		    }
		  </script>
		  </head>
		  <body>
		    <h2>PayU Form</h2>
		    <br/>   
			<form action={{ action }} method="post" name="payuForm">
			    <input type="hidden" name="key" value="{{ MERCHANT_KEY }}" />
			    <input type="hidden" name="hash_string" value="{{ hash_string }}" />
			    <input type="hidden" name="hash" value="{{ hashh }}"/>
			    <input type="hidden" name="amount" value="{{ posted.amount|default:'' }}" />
			    <input type="hidden" name="posted" value="{{ posted }}"/>
			    <input type="hidden" name="txnid" value="{{ txnid }}" />
			    <input type="hidden" name="firstname" id="firstname" value="{{ posted.firstname|default:'' }}" />
			    <input  type="hidden" name="email" id="email" value="{{ posted.email|default:'' }}" />
			    <input type="hidden" name="phone" value="{{ posted.phone|default:'' }}" />
			    <input  type="hidden" name="productinfo" value="{{ posted.productinfo|default:'' }}">
			    <input type="hidden" name="surl" value="{{ posted.surl }}" size="64" />
			    <input type="hidden" name="furl" value="{{ posted.furl }}" size="64" />
			    <input type="hidden" name="service_provider" value="{{service_provider}}" size="64" />
			    <input type="submit" value="Submit" />
			</tr>
		      </table>
		    </form>
		  </body>
		</html>

```
	 
you can write some javascript tweks to submit a form automaticaly. here is clickble mode.


##Verify Hash

This functionality is  verifying the transaction is done by our server.
 
Once we made the transaction , which will fail/success the payu will 
 send the HASH value along with the response.
 We can calculate the hash value with our server also , then we 
 can match with the hash which is from PAYU, if it's match we can conclude that 
 the transaction done by our end and the transaction is valid.
 
 ```
 @csrf_exempt
def payu_success(request):
    return_data = request.POST.dict()
    # Verifying hash
    # Will return status for the hash whether it's True|False,
    # What is the Hashsequence we used for creating Hash
    # The hash which we created.
    # If he hash status is True, make the transaction as SUCCESS Transaction
    hashstatus, hashsequence, our_hash = pm.payu_verifyhash(request.POST.dict())
    print("Verify Hash Value with posted from payu response is valid", hashstatus)
    print("Hashsequence which we created", hashsequence)
    ## printing the hash which we have recived from payu and what we have created is matching
    print("POSted hash from payu", return_data['hash'])
    print("The hash which we created with the same data for validation", our_hash)
    if hashstatus:
        return render(request, 'payu/sucess.html',
                      {"txnid": return_data.get('txnid', ''), "status": return_data.get('status', ''),
                       "amount": return_data('amount', '')})
    return JsonResponse({"status": "Error", "message": "Wrong Transaction"})


@csrf_exempt
def payu_failure(request):
    return_data = request.POST.dict()
    #Verifying hash
    # Will return status for the hash whether it's True|False,
    # What is the Hashsequence we used for creating Hash
    # The hash which we created.
    # If he hash status is True, make the transaction as SUCCESS Transaction
    hashstatus, hashsequence, our_hash = pm.payu_verifyhash(request.POST.dict())
    print("Verify Hash Value with posted from payu response is valid", hashstatus)
    print("Hashsequence which we created", hashsequence)
    ## printing the hash which we have recived from payu and what we have created is matching
    print("POSted hash from payu", return_data['hash'])
    print("The hash which we created with the same data for validation", our_hash)
    if hashstatus:
        return render(request, 'payu/failure.html',
                      {"txnid": return_data.get('txnid', ''), "status": return_data.get('status', ''),
                       "amount": return_data('amount', '')})
    return JsonResponse({"status": "Error", "message": "Wrong Transaction"})
 
 ```
 
 
 
 
 





