# -*- coding: utf-8 -*-

"""Top-level package for paywix."""

__author__ = """Renjith S Raj"""
__email__ = 'renjithsraj@live.com'
__version__ = '1.0.2    '

# Payment gateway files
from paywix import payu


# Route to Payu

class PayMentManager(object):

    def payu_transaction(self, data):
        data = payu.initiate(data)
        return data

    def payu_verifyhash(self, data):
        data = payu.check_hash(data)
        return data
