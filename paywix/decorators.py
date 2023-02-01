from functools import wraps
from paywix.config import PAYU_CONFIGS
from paywix.exceptions import PaywixValidationException


def validate_params(pg, action):
    """
        validate the function based on the args
        args[0] => payment gateway
        args[1] => action
        Kwargs => requested params
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            requested_cols, __mandatory_cols = [], []
            if (pg == 'payu') and (action == 'transaction'):
                __mandatory_cols = PAYU_CONFIGS[action]
                for req_arg in __mandatory_cols:
                    if not kwargs.get(req_arg):
                        requested_cols.append(req_arg)

            if len(requested_cols) != 0:
                raise PaywixValidationException(
                    __mandatory_cols,
                    requested_cols,
                    pg,
                    action
                )
            return func(*args, **kwargs)
        return wrapper
    return decorator
