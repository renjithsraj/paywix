# Paytm Integration with Paywix

This document  contins the integration steps for the paytm payment configuration on python based applications.

## Initial Configuration
If you want to configure paytm in your application you must install  pycrypto, or else will get no module found error.

```shell
pip install pycrypto
```
## How to config paytm with  application

This section will give you the detailed explanation for the config paywix on python based applications.  

```python
PAYTM_CONFIG = {
    'merchant_id': "kGuPMZ17441871743529",
    'merchant_key': 'frmTjdL@1fyhBzAr',
    'website': 'WEBSTAGING',
    'channel_id': 'WEB',
    'industry_type_id': 'Retail'
}
```
Import Paytm from paywix  and  follow below methods to integrate paytm on your application

```python
from paywix.paytm import Paytm
paytm = Paytm(paytm_config['merchant_id'],  paytm_config['merchant_key'], mode='test')
```
# API Referance 
Here will give you paytm methods

## 1. paytm.checkout_data()
This method will generate checkout_data for the payment transactions, there are two type of response will get it from this function with use of `is_html=False | True` 
- `is_html = True ->` Response will be `HTML` string you can use this for render as Httpresponse 
- `is_html = False ->` Response will be checkout data with checksum , you can render this  data to paytm template in your template folder (detail will give below)
- callback_url -> where you want to redirect after done the payment transaction

```python
data = {
            'website': paytm_config['website'],
            'industry_type_id': paytm_config['industry_type_id'], 
            'channel_id': paytm_config['channel_id'],
            'order_id': "12345678901235467",
            'cust_id': "renjithsraj@live.com", 
            'txn_amount': "10.0", 
            'callback_url': "http://127.0.0.1:8000/paytm_callback",
            'mobile_no': "9746272610"
        }
# Generate HTML Page
html = paytm.checkout_data(data, is_html=True)
return HttpResponse(html, content_type='text/html')    # django
```
###### HTML response (is_html = True)
``` html
html page
html>
<head>
   <meta http-equiv="Content-Type" content="text/html; charset=ISO-8859-1">
   <title>Paytm Secure Online Payment Gateway</title>
</head>
<body>
   <table align='center'>
      <tr>
         <td><STRONG>Transaction is being processed,</STRONG></td>
      </tr>
      <tr>
         <td><font color='blue'>Please wait ...</font></td>
      </tr>
      <tr>
         <td>(Please do not press 'Refresh' or 'Back' button</td>
      </tr>
   </table>
   <form method="post" action=https://securegw-stage.paytm.in/order/process name="paytm">
      <table border="1">
         <tbody><input type='hidden' name='WEBSITE' value='WEBSTAGING'><input type='hidden' name='INDUSTRY_TYPE_ID' value='Retail'><input type='hidden' name='CHANNEL_ID' value='WEB'><input type='hidden' name='ORDER_ID' value='12345678901235467'><input type='hidden' name='CUST_ID' value='renjithsraj@live.com'><input type='hidden' name='TXN_AMOUNT' value='10.0'><input type='hidden' name='CALLBACK_URL' value='http://127.0.0.1:8000/paytm_callback'><input type='hidden' name='MOBILE_NO' value='9746272610'><input type='hidden' name='MID' value='kGuPMZ17441871743529'><input type='hidden' name='CHECKSUMHASH' value='Lr58IEtDktBALBI7Bp08NkRMV0j6R4CNln9Fw93INZUPKNnbPz/dSLQ++CQ6K9p1jYTBugarscDQg24077N96M/PJVTGJuJ+yyUWkJcp7dc='>
         </tbody>
      </table>
      <script type="text/javascript">
         document.paytm.submit();
      </script>
   </form>
</body>
</html>
```

```python
# Generate Checkout data
 payment_Data = paytm.checkout_data(data, is_html=False)
 ```
 ###### checkout_data (is_html=False)
 ```python
 
{'WEBSITE': 'WEBSTAGING', 
'INDUSTRY_TYPE_ID': 'Retail', 
'CHANNEL_ID': 'WEB', 
'ORDER_ID': '12345678901235467', 
'CUST_ID': 'renjithsraj@live.com', 
'TXN_AMOUNT': '10.0', 'CALLBACK_URL': 'http://127.0.0.1:8000/paytm_callback', 
'MOBILE_NO': '9746272610', 'MID': 'kGuPMZ17441871743529', 
'CHECKSUMHASH': 'CcbT9oeNO/Ttwc1qg0F0hTikc9Ih6An7RmHF0tPfi7WfkWPPekvhLI7XhNtGwntgWrPsFPr2zNkDTL0lj1Nw8yzIbJVKGoRFncF1+ssbtfQ='}

You can pass this to the paytm_payment .html page which you have created in the template folder.

```
