from backend.blockchain.block import Block

class Blockchain:
    """
    A public ledger of transactions
    Implemented as a list of blocks, which are datasets of transactions
    """

    def __init__(self):
        self.chain = [Block.seed()]

    def addBlock(self, data):
        self.chain.append(Block.mineBlock(self.chain[-1],data))

    def __repr__(self):
        return f'Blockchain: {self.chain}'

    def replaceChain(self, chain):
        """
        Replace local chain with incoming if these rules apply:
            - Incoming chain is longer than local chain
            - Incoming chain is properly formatted
        """

        if len(chain) <= len(self.chain):
            raise Exception('Will NOT replace. Incoming chain must be longer than local chain.')
        
        try:
            Blockchain.isValidChain(chain)
        except Exception as e:
            raise Exception(f'Will NOT replace. Invalid incoming chain: {e}')

        self.chain = chain

    def toJson(self):
        """
        Serialize the blockchain into a list of blocks.
        """
        return list(map(lambda block: block.toJson(), self.chain))

    @staticmethod
    def fromJson(chainJson):
        """
        Deserialize a list of serialized blocks into a blockchain instance.
        The result contains a chain list of block instances.
        """
        blockchain = Blockchain()
        blockchain.chain = list(map(lambda blockJson: Block.fromJson(blockJson), chainJson))

        return blockchain

    @staticmethod
    def isValidChain(chain):
        """
        Validate the incoming chain.
        Enforce rules of the blockchain:
          - Chain must start with the seed block
          - Blocks must be correctly formatted
        """
        if chain[0] != Block.seed():
            raise Exception('Invalid Seed block.')

        for i in range(1, len(chain)):
            block = chain[i]
            previousBlock = chain[i-1]
            Block.isValidBlock(previousBlock, block)


def main():
    blockchain = Blockchain()        
    blockchain.addBlock('one')
    blockchain.addBlock('two')

    print(blockchain)

if __name__ == '__main__':
     main()