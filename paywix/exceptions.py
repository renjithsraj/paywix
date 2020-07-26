
class AccessModeException(Exception):
    def __int__(self, args):
        pass

    def __str__(self):
        mode = self.args[0]
        return f'{mode} not valid, valid modes are ["test", "live"]'


class RequiredDataException(Exception):

    def __init__(self, gateway, txn_type, params):
        self.gateway = gateway
        self.txn_type = txn_type
        self.params = params

    def __str__(self):
        return f'To configure {self.txn_type} with {self.gateway} required {self.params}'
