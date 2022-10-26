import json
import uuid
from backend.config import STARTING_BALANCE
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.asymmetric.utils import(
    encode_dss_signature,
    decode_dss_signature
)
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.exceptions import InvalidSignature

class Wallet:
    """
    An individual wallet for currency user.
    Keeps track of user's balance.
    Allows a user to authorize transactions.
    """
    def __init__(self):
        self.address = str(uuid.uuid4())
        self.balance = STARTING_BALANCE
        self.privateKey = ec.generate_private_key(ec.SECP256K1(), default_backend())
        self.publicKey = self.privateKey.public_key()
        self.serializePublicKey()

    def sign(self, data):
        """
        Generates a signature based on the data, and using the local private key.
        """
        return decode_dss_signature(self.privateKey.sign(json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA512())))

    def serializePublicKey(self):
        self.publicKey = self.publicKey.public_bytes(encoding = serialization.Encoding.PEM, format = serialization.PublicFormat.SubjectPublicKeyInfo).decode('utf-8')

    @staticmethod
    def verify(publicKey, data, signature):
        """
        Verify a signature based on the original public key and data.
        """
        deserializedPublicKey = serialization.load_pem_public_key(
            publicKey.encode('utf-8'),
            default_backend()
        )

        (r, s) = signature

        try:
            deserializedPublicKey.verify(encode_dss_signature(r, s), json.dumps(data).encode('utf-8'), ec.ECDSA(hashes.SHA512()))

            return True
        except InvalidSignature:
            return False

def main():
    wallet = Wallet()
    print(f'wallet.__dict__: {wallet.__dict__}')
    data = {'foo': 'bar'}
    signature = wallet.sign(data)
    print(f'signature: {signature}')

    shouldBeValid = Wallet.verify(wallet.publicKey, data, signature)

    print(f'shouldBeValid: {shouldBeValid}')

    shouldBeINValid = Wallet.verify(Wallet().publicKey, data, signature)

    print(f'shouldBeINValid: {shouldBeINValid}')

if __name__ == '__main__':
    main()