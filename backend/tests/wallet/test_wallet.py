from backend.wallet.wallet import Wallet

def test_verifyValidSignature():
    data = {'foo': 'bar-data'}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert Wallet.verify(wallet.publicKey, data, signature)

def test_verifyInvalidSignature():
    data = {'foo': 'bar-data'}
    wallet = Wallet()
    signature = wallet.sign(data)

    assert not Wallet.verify(Wallet().publicKey, data, signature)