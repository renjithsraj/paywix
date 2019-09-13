from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def payu_success(request):
    return JsonResponse(request.POST)


@csrf_exempt
def payu_failure(request):
    return JsonResponse(request.POST)




































stripe_token = getattr(settings, 'PAY_WIX_STRIPE_TOKEN', False)

braintree_pg = BraintreePay(
    env='SANDBOX', merchant_id='d382xqn5f2wc9m4j',
    public_key='4h6h6bn6r2vd8wsm',
    private_key="d2b96d389934ac7a3af2cb8d935fe1ac"
)




def paywix_ajax_handle(request):
    rq = request.POST
    if request.method == 'POST':
        rq = request.POST.get
        required_params = ['description', 'amount', 'order_id', 'currency',
                    "token[id]"]
        for param in required_params:
            if not rq(param):
                raise ValueError("{0} doesn't empty".format(param))
        if not stripe_token:
            raise ValueError('PAYWIX_STRIPE_TOKEN is missing:\
                    please insert valid stripe secret key')
        try:
            stripe.api_key = stripe_token
            charge = stripe.Charge.create(
                amount = int(rq('amount'))*100,
                currency= rq('currency'),
                description= rq('description'),
                source= rq('token[id]'),
                metadata = {'order_id': rq('order_id')}
            )
            print (charge)
        except stripe.error.CardError as e:
            body = e.json_body
            err  = body.get('error', {})
            messages.error(request, "status : {1} <br> message : {2}".format(e.http_status, err.get('message')))
        except stripe.error.RateLimitError as e:
            body = e.json_body
            err  = body.get('error', {})
            messages.error(request, "status : {1} <br> message : {2}".format(e.http_status, err.get('message')))
        except stripe.error.InvalidRequestError as e:
            body = e.json_body
            err  = body.get('error', {})
            messages.error(request, "status : {1} <br> message : {2}".format(e.http_status, err.get('message')))
        except stripe.error.AuthenticationError as e:
            body = e.json_body
            err  = body.get('error', {})
            messages.error(request, "status : {1} <br> message : {2}".format(e.http_status, err.get('message')))
        except stripe.error.APIConnectionError as e:
            body = e.json_body
            err  = body.get('error', {})
            messages.error(request, "status : {1} <br> message : {2}".format(e.http_status, err.get('message')))
        except stripe.error.StripeError as e:
            body = e.json_body
            err  = body.get('error', {})
            messages.error(request, "status : {1} <br> message : {2}".format(e.http_status, err.get('message')))
        except Exception as e:
            messages.success(request, "status : {1} <br> message : {2}".format("failure", "Something went wrong"))
    else:
        raise PermissionDenied

def paywix_braintree_pay(request):
    if request.method == 'POST':
        token = request.POST.get('payload')
        result = braintree_pg.transact({
        'amount': "500",
        'payment_method_nonce': token,
        'options': {
            "submit_for_settlement": True
        }
        })

    if result.is_success or result.transaction:
       print(result)
    else:
        for x in result.errors.deep_errors:
            print (x)
