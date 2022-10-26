import time

from backend.util.cryptohash import cryptoHash
from backend.util.hexToBinary import hexToBinary
from backend.config import MINE_RATE #, HALVING_BLOCK, NUMBER_OF_HALVINGS

INITIAL_DIFFICULTY = 3

SEED_DATA = {
    'blockNumber': 1,
    'timestamp': 1,
    'previousHash': '0Hash',
    'hash': f'seedHash-0000000001012023',
    'data': [],
    'difficulty': INITIAL_DIFFICULTY,
    'nonce': 'seedNonce'
    
}

class Block:
    """
    The block is the main unit of storage.
    Stores transactions in a blockchain that supports a crptocurrency.
    """

    def __init__(self, blockNumber, timestamp, previousHash, hash, data, difficulty, nonce):
        self.blockNumber = blockNumber
        self.timestamp = timestamp
        self.previousHash = previousHash
        self.hash = hash
        self.data = data
        self.difficulty = difficulty
        self.nonce = nonce

    def __repr__(self):
        return (
            'Block( '
            f'Block Number {self.blockNumber}, '
            f'timestamp: {self.timestamp}, '
            f'previous hash: {self.previousHash}, '
            f'hash: {self.hash}, '
            f'data: {self.data}, '
            f'difficulty: {self.difficulty}, '
            f'nonce: {self.nonce}'
            ' )'
        )

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def toJson(self):
        """
        Serialize the block into a dictionary of its attributes
        """
        return self.__dict__

    @staticmethod
    def mineBlock(previousBlock, data):
        """
        Mines a block based on the previousBlock and given data, until a block hash found that meets the leading zeros required for proof of work.
        """

        blockNumber = previousBlock.blockNumber + 1
        timestamp = time.time_ns()
        previousHash = previousBlock.hash
        difficulty = Block.adjustDifficulty(previousBlock, timestamp)
        nonce = 0
        hash = cryptoHash(blockNumber, timestamp, previousHash, data, difficulty, nonce)

        while hexToBinary(hash) [0: difficulty] != '0' * difficulty:
            nonce += 1
            timestamp = time.time_ns()
            difficulty = Block.adjustDifficulty(previousBlock, timestamp)
            hash = cryptoHash(blockNumber, timestamp, previousHash, data, difficulty, nonce)

        return Block(blockNumber, timestamp, previousHash, hash, data, difficulty, nonce)


    @staticmethod
    def seed():
        """
        Initialize blockchain's run-once vlaues.
        Generate the blockchain's seed block.
        """

        return Block(**SEED_DATA)

    @staticmethod
    def fromJson(blockJson):
        """
        Deserialize a block Json representation back into a block instance.
        """

        return Block(**blockJson)

    @staticmethod
    def adjustDifficulty(previousBlock, newTimestamp):
        """
        Calculate adjusted difficulty according to MINE_RATE and according to HALVING_BLOCK.

        Doubles the difficulty if blockNumber is divisible by HALVING_BLOCK.

        Increases difficulty for quickly mined blocks.
        Lowers difficulty for slowly mined blocks.
        """

        # if ((previousBlock.blockNumber + HALVING_BLOCK +1) % HALVING_BLOCK) == 0:
        #     NUMBER_OF_HALVINGS += 1

        #     return (previousBlock.difficulty * 2)

        if (newTimestamp - previousBlock.timestamp) < MINE_RATE:
            return previousBlock.difficulty + 1

        if(previousBlock.difficulty -1) > 0:
            return previousBlock.difficulty - 1

        return 1

    @staticmethod
    def isValidBlock(previousBlock, block):

        #NEEDS TO BE CHECKED FOR HALVING DIFFICULTY IMPLEMENTATION.

        """
        Block validation rules:
            1. Block must have the proper previousHash reference
            2. Block must meet proof of work difficulty requirements.
            3. Block difficulty must have only been adjust by 1.
            4. Block hash must a valid combination with the block's fields.
        """
        if block.previousHash != previousBlock.hash:
            raise Exception('PreviousHash is not correct')

        if hexToBinary(block.hash)[0:block.difficulty] != '0' * block.difficulty:
            raise Exception('Proof of work requirement was not met.')

        if abs(previousBlock.difficulty - block.difficulty) > 1:
            raise Exception ('Block difficulty must only be adjusted by 1.')

        reconstructedHash = cryptoHash(
            block.blockNumber,
            block.timestamp,
            block.previousHash,
            block.data,
            block.nonce,
            block.difficulty
        )
        if block.hash != reconstructedHash:
            raise Exception('Block hash is not correct.')




def main():
    seedBlock = Block.seed()
    badBlock = Block.mineBlock(seedBlock, 'blabla')
    badBlock.previousHash = 'evilData'

    try:
        Block.isValidBlock(seedBlock, badBlock)
    except Exception as e:
        print(f'isValidBlock: {e}')

if __name__ == '__main__':
     main()