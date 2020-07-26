payu_config = {
    "test": "https://sandboxsecure.payu.in/_payment",
    "live": "https://secure.payu.in/_payment",
    "api_test": "https://test.payumoney.com/payment/",
    "api_live": "https://www.payumoney.com/payment/",
}

required_data = {
    "payu_request": ['txnid', 'amount', 'productinfo', 'firstname', 'email'],
    "payu_payment_resp": ['transaction_ids']
}
