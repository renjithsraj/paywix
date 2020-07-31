from functools import wraps
from paywix.utils import required_data
from paywix.exceptions import RequiredDataException


class validate_params(object):

    def __init__(self, req_cat, gateway, txn_type):
        self.category = req_cat
        self.gateway = gateway
        self.txn_type = txn_type

    def __call__(self, func):
        @wraps(func)
        def callable(*args, **kwargs):
            missing_data = [req_item for req_item in required_data.get(
                self.category) if not kwargs.get(req_item)]
            if len(missing_data) > 0:
                raise RequiredDataException(
                    self.gateway, self.txn_type, missing_data)
            return func(*args, **kwargs)
        return callable
