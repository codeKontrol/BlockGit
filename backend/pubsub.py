import time
from pubnub.pubnub import PubNub
from pubnub.pnconfiguration import PNConfiguration
from pubnub.callbacks import SubscribeCallback
from backend.blockchain.block import Block
from backend.wallet.transaction import Transaction

pnconfig = PNConfiguration()
pnconfig.subscribe_key = 'sub-c-e9287a9a-df2a-4c28-b7a4-2cb79f82d93e'
pnconfig.publish_key = 'pub-c-b6c6a446-3f08-4226-af3a-2fa205e4b13f'

CHANNELS = {
    'TEST': 'TEST',
    'BLOCK': 'BLOCK',
    'TRANSACTION': 'TRANSACTION'
}


class Listener(SubscribeCallback):
    def __init__(self, blockchain, transactionPool):
        self.blockchain = blockchain
        self.transactionPool = transactionPool

    def message(self, pubnub, message_object):
        print(f'\n-- Channel: {message_object.channel} | Message: {message_object.message}')
        if message_object.channel == CHANNELS['BLOCK']:
            block = Block.fromJson(message_object.message)
            #Copy the existing blockchain into a new variable.
            potentialChain = self.blockchain.chain[:]
            potentialChain.append(block)

            try:
                self.blockchain.replaceChain(potentialChain)
                print(f'\n-- Local chain replacement SUCCESSFUL.')
            except Exception as e:
                print(f'\n-- Did NOT replace the chain: {e}')

        elif message_object.channel == CHANNELS['TRANSACTION']:
            transaction = Transaction.fromJson(message_object.message)
            self.transactionPool.setTransaction(transaction)
            print('\n-- New transaction set in the transactions pool')


class PubSub():
    """
    Handles the Publish\Subscribe layer of the application.
    Provides communication to the nodes of the blockchain network.
    """
    def __init__(self, blockchain, transactionPool):
        self.pubnub = PubNub(pnconfig)
        self.pubnub.subscribe().channels(CHANNELS.values()).execute()
        self.pubnub.add_listener(Listener(blockchain, transactionPool))

    def publish(self, channel, message):
        """
        Publish the message object to the channel.
        """
        #self.pubnub.publish().channel(channel).message(message).sync()
        self.pubnub.unsubscribe().channels([channel]).execute()
        self.pubnub.publish().channel(channel).message(message).sync()
        self.pubnub.subscribe().channels([channel]).execute()
        

    def broadcastBlock(self, block):
        """
        Broadcast a block to all nodes
        """
        self.publish(CHANNELS['BLOCK'], block.toJson())


    def broadcastTransaction(self, transaction):
        """
        Broadcast a transaction to all nodes
        """
        self.publish(CHANNELS['TRANSACTION'], transaction.toJson())



def main():
    pubsub = PubSub(blockchain)
    time.sleep(1)
    pubsub.publish(CHANNELS['TEST'], {'foo': 'bar'})


if __name__ == '__main__':
    main()

