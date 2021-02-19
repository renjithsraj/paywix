import base64
import string
import random
import hashlib
import sys
from Crypto.Cipher import AES


class PaytmChecksum():
    def __init__(self):
        self.iv = '@@@@&&&&####$$$$'
        self.BLOCK_SIZE = 16
        if (sys.version_info > (3, 0)):
            self.__pad__ = lambda s: bytes(
                s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * chr(
                    self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE), 'utf-8')
        else:
            self.__pad__ = lambda s: s + \
                (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * \
                chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)
        self.__unpad__ = lambda s: s[0:-ord(s[-1])]
        self.mode_cbc = AES.MODE_CBC

    def encrypt(self, input_string, key):
        input_string = self.__pad__(input_string)
        c = AES.new(key.encode("utf8"), self.mode_cbc, self.iv.encode("utf8"))
        input_string = c.encrypt(input_string)
        input_string = base64.b64encode(input_string)
        return input_string.decode("UTF-8")

    def decrypt(self, encrypted_string, key):
        encrypted_string = base64.b64decode(encrypted_string)
        c = AES.new(key.encode("utf8"), self.mode_cbc, self.iv.encode("utf8"))
        param = c.decrypt(encrypted_string)
        if type(param) is bytes:
            param = param.decode()
        return self.__unpad__(param)

    def generate_signature(self, params, key):
        if type(params) not in [dict, str]:
            raise TypeError(
                f"string or dict expected, {str(type(params))} given")
        if type(params) is dict:
            params = self.get_string_by_params(params)
        return self.generate_signature_by_string(params, key)

    def get_string_by_params(self, params):
        params_string = []
        for key in sorted(params.keys()):
            value = params[key] if params[
                key] is not None and params[key].lower() != "null" else ""
            params_string.append(str(value))
        return '|'.join(params_string)

    def generate_signature_by_string(self, params, key):
        salt = self.generate_random_string(4)
        return self.calculate_checksum(params, key, salt)

    def generate_random_string(self, length):
        chars = string.ascii_uppercase + string.digits + string.ascii_lowercase
        return ''.join(random.choice(chars) for _ in range(length))

    def calculate_checksum(self, params, key, salt):
        hash_string = self.calculate_hash(params, salt)
        return self.encrypt(hash_string, key)

    def calculate_hash(self, params, salt):
        final_string = '%s|%s' % (params, salt)
        hasher = hashlib.sha256(final_string.encode())
        return hasher.hexdigest() + salt

    def verify_signature(self, params, key, checksum):
        if type(params) not in [dict, str]:
            raise TypeError(
                f"string or dict expected, {str(type(params))} given")

        if "CHECKSUMHASH" in params:
            del params["CHECKSUMHASH"]

        if type(params) is dict:
            params = self.get_string_by_params(params)
        return self.verify_signature_by_string(params, key, checksum)

    def verify_signature_by_string(self, params, key, checksum):
        paytm_hash = self.decrypt(checksum, key)
        salt = paytm_hash[-4:]
        calculated_hash = self.calculate_hash(params, salt)
        signatute_data = {
            "is_verified": paytm_hash == calculated_hash,
            "paytm_hash": paytm_hash,
            "calculated_hash": calculated_hash
        }
        return signatute_data
