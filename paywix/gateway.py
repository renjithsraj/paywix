from abc import ABC, abstractmethod


class Gateway(ABC):

    @abstractmethod
    def generate_hash(self, *args, **kwargs):
        pass

    @abstractmethod
    def transaction(self, *args, **kwargs):
        pass

    @abstractmethod
    def verify(self, *args, **kwargs):
        pass

    @abstractmethod
    def header(self, *args, **kwargs):
        pass

    @abstractmethod
    def post(self, *args, **kwargs):
        pass

    @abstractmethod
    def response(self, *args, **kwargs):
        pass

    @abstractmethod
    def txn_status(self, *args, **kwargs):
        pass

    @abstractmethod
    def refund(self, *args, **kwargs):
        pass

    @abstractmethod
    def refund_details(self, *args, **kwargs):
        pass
