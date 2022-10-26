
class TransactionPool:
    def __init__(self):
        self.transactionMap = {}

    def setTransaction(self, transaction):
        """
        Set a transaction in the transactions pool.
        """
        self.transactionMap[transaction.id] = transaction

    def existingTransaction(self, address):
        """
        Finds a transaction generated by the address in the transactions pool.
        """
        for transaction in self.transactionMap.values():
            if transaction.input['address'] == address:
                return transaction