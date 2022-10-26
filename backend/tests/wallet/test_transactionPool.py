from backend.wallet.transactionPool import TransactionPool
from backend.wallet.transaction import Transaction
from backend.wallet.wallet import Wallet

def test_setTransaction():
    tp = TransactionPool()
    transaction = Transaction(Wallet(), 'recipient', 1)
    tp.setTransaction(transaction)

    assert tp.transactionMap[transaction.id] == transaction