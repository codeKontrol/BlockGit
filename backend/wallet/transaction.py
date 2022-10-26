import uuid
import time
from backend.wallet.wallet import Wallet

class Transaction:
    """
    Document a currency exchange from a sender to one or more recipients.
    """
    def __init__(self,
        sender = None,
        recipient = None,
        amount = None,
        id = None,
        output = None,
        input = None
    ):
        self.id = id or str(uuid.uuid4())
        self.output = output or self.createOutput(
            sender,
            recipient,
            amount
        )
        self.input = input or self.createInput(sender, self.output)

    def createOutput(self, sender, recipient, amount):
        """
        Structure the output data for the transaction.
        """
        #totalTXamount = teamFee + txFee + daoFee + amount
        if amount > sender.balance:
            raise Exception('Not enough balance to complete the transaction.')

        output = {}
        #output[teamWallet.address] = teamFee
        #output[minerWallet.address] = txFee
        #output[daoWallet] = daoFee

        output[recipient] = amount
        output[sender.address] = sender.balance - amount


        return output

    def createInput(self, sender, output):
        """
        Structure the input data for the transaction.
        Sign the transaction and include the sender's public key and address.
        """

        return{
            'timestamp': time.time_ns(),
            'amount': sender.balance,
            'address': sender.address,
            'publicKey': sender.publicKey,
            'signature': sender.sign(output)
        }

    def update(self, sender, recipient, amount):
        """
        Update transaction with existing or new recipients.
        """
        if amount > self.output[sender.address]:
            raise Exception('Not enough balance to complete the transaction.')

        if recipient in self.output:
            self.output[recipient] = self.output[recipient] + amount
        else:
            self.output[recipient] = amount

        self.output[sender.address] = self.output[sender.address] - amount

        self.input = self.createInput(sender, self.output)

    def toJson(self):
        """
        Serialize a transaction.
        """
        return self.__dict__

    @staticmethod
    def fromJson(transactionJson):
        """
        Deserialize a transaction's json representation back into a Transaction instance.
        """
        return Transaction(**transactionJson)

    @staticmethod
    def isValidTransaction(transaction):
        """
        Validates a transaction.
        Raises an exception for invalid transactions.
        """
        outputTotal = sum(transaction.output.values())
        if transaction.input['amount'] != outputTotal:
            raise Exception('Invalid transaction due to output values.')

        if not Wallet.verify(
            transaction.input['publicKey'],
            transaction.output,
            transaction.input['signature']
        ):
            raise Exception('Invalid signature.')
            

def main():
    transaction = Transaction(Wallet(), 'recipient', 15)
    print(f'transaction.__dict__: {transaction.__dict__}')

    transactionJson = transaction.toJson()
    restoredTransaction = Transaction.fromJson(transactionJson)
    print(f'restoredTransaction.__dict__: {restoredTransaction.__dict__}')


if __name__ == '__main__':
    main()