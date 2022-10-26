import pytest
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def test_transaction():
    sender = Wallet()
    recipient = 'recipient'
    amount = 50
    transaction = Transaction(sender, recipient, amount)

    assert transaction.output[recipient] == amount
    assert transaction.output[sender.address] == sender.balance - amount

    assert 'timestamp'in transaction.input
    assert transaction.input['amount'] == sender.balance
    assert transaction.input['address'] == sender.address
    assert transaction.input['publicKey'] == sender.publicKey

    assert Wallet.verify(
        transaction.input['publicKey'],
        transaction.output,
        transaction.input['signature']
    )

def test_transactionExceedsBalance():
    with pytest.raises(Exception, match='Not enough balance to complete the transaction.'):
        Transaction(Wallet(), 'recipient', 1001)

def test_transactionUpdateExceedsBalance():
    sender = Wallet()
    transaction = Transaction(sender, 'recipient', 55)

    with pytest.raises(Exception, match='Not enough balance to complete the transaction.'):
        transaction.update(sender, 'another_recipient', 1001)

def test_transactionUpdate():
    sender = Wallet()
    recipient1 = 'recipient 1'
    amount1 = 50
    recipient2 = 'recipient 2'
    amount2 = 75
    transaction = Transaction(sender, recipient1, amount1)
    transaction.update(sender, recipient2, amount2)

    assert transaction.output[recipient2] == amount2
    assert transaction.output[sender.address] == sender.balance - amount1 - amount2
    assert Wallet.verify(
    transaction.input['publicKey'],
    transaction.output,
    transaction.input['signature']
    )

    anotherTxTo1 = 24
    transaction.update(sender, recipient1, anotherTxTo1)

    assert transaction.output[recipient1] == amount1 + anotherTxTo1
    assert transaction.output[sender.address] == sender.balance - amount1 - amount2 - anotherTxTo1
    assert Wallet.verify(
    transaction.input['publicKey'],
    transaction.output,
    transaction.input['signature']
    )

def test_validTransaction():
    Transaction.isValidTransaction(Transaction(Wallet(), 'recipient', 50))

def test_invalidOutputsTransaction():
    sender = Wallet()
    transaction = Transaction(sender, 'recipient', 50)
    transaction.output[sender.address] = 1005

    with pytest.raises(Exception, match='Invalid transaction due to output values.'):
        Transaction.isValidTransaction(transaction)

def test_invalidSignatureTransaction():
    sender = Wallet()
    transaction = Transaction(sender, 'recipient', 50)
    transaction.input['signature'] = Wallet().sign(transaction.output)

    with pytest.raises(Exception, match='Invalid signature.'):
        Transaction.isValidTransaction(transaction)

