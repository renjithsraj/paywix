payu_config = {
    "test": "https://sandboxsecure.payu.in/_payment",
    "live": "https://secure.payu.in/_payment",
    "api_test": "https://www.payumoney.com/sandbox/",
    "api_live": "https://www.payumoney.com/",
    "payu_api_ref": "http://www.payumoney.com/",
}

service_urls = {
    "getPaymentResponse": "payment/op/getPaymentResponse?merchantKey={key}&merchantTransactionIds={ids}",
    "chkMerchantTxnStatus": "payment/payment/chkMerchantTxnStatus?merchantKey={key}&merchantTransactionIds={ids}",
    "refundPayment": "treasury/merchant/refundPayment?merchantKey={key}&paymentId={payu_id}&refundAmount={amount}",
    "getRefundDetails": "treasury/ext/merchant/getRefundDetails?merchantKey={key}&refundId={refund_id}",
    "getRefundDetailsByPayment": "treasury/ext/merchant/getRefundDetailsByPayment?merchantKey={key}&paymentId={payu_id}",
}


cashfree_config = {
    "test": "https://www.cashfree.com/checkout/post/submit",
    "live": "https://test.cashfree.com/billpay/checkout/post/submit",
    "currency_details": {
        "INR": "Indian Rupee",
        "USD": "US Dollar",
        "BDT": "Bangladesh Taka",
        "GBP": "Pound Sterling",
        "AED": "UAE Dirham",
        "AUD": "Australian Dollar",
        "BHD": "Bahraini Dinar",
        "CAD": "Canadian Dollar",
        "CHF": "Swiss Franc",
        "DKK": "Danish Krone",
        "EUR": "Euro",
        "HKD": "Hong Kong Dollar",
        "JPY": "Japanese Yen",
        "KES": "Kenya Shiling",
        "KWD": "Kuwaiti Dinar",
        "LKR": "Srilanka Rupee",
        "MUR": "Mauritius Rupee",
        "MYR": "Malaysian Ringgit",
        "NOK": "Norwegian Krone",
        "NPR": "Nepalese Rupee",
        "NZD": "New Zealand Dollar",
        "OMR": "Rial Omani",
        "QAR": "Qatari Rial",
        "SAR": "Saudi Riyal",
        "SEK": "Swedish Krona",
        "SGD": "Singapore Dollar",
        "THB": "Thai Baht",
        "ZAR": "South African Rand"
    }
}


required_data = {
    "payu_request": ['txnid', 'amount', 'productinfo', 'firstname', 'email'],
    "payu_payment_resp": ['transaction_ids'],
    "cashfree_request": ['order_id', 'amount', 'name', 'phone', 'email']
}


def payu_url_generator(command, mode, refund_api=False):
    base_url = payu_config.get(mode)
    if refund_api:
        base_url = payu_config.get('payu_api_ref')
    base_url += service_urls[command]
    return base_url


def get_casfree_currency_data():
    return cashfree_config['currency_details']
