paywix
=====

`PayWix` is a python wrapper for handle payment gateway integrations in Django based applications, This is the advanced version of `payu_biz` in this package only support for `payu` payment gateway but in the case of `paywix`, it will support almost all the payment gateways. so you don't need to much worry about the integrations part, Just import it and go on.

The beta version 1.0.2 is deployed in PYPI with the support of payu payment gateway.

Note
----
* This package is working fine on Python3 with django2.X versions. not compatable with previous versions

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

This package will include
-------------------------
Paywix providing following payment gateways support.
* Payu
* Cashfree
* JustPay
* PayTm
* BrainTree
* etc

Features
--------
* [Payu Payment gateway Integration in Django](../master/payu.md)
* [Cashfree Payment gateway Integration in Django](../master/cashfree.md)


Notes
-------
* The Package is working fine with latest version of django and python3.
* It's in developement mode but for payu make transaction/verify transaction is working fine.
