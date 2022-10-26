from backend.blockchain.blockchain import Blockchain
from backend.blockchain.block import SEED_DATA

import pytest

def test_blockchainInstance():
    blockchain = Blockchain()
    assert blockchain.chain[0].hash == SEED_DATA['hash']

def test_addBlock():
    blockchain = Blockchain()
    data = 'test-data'
    blockchain.addBlock(data)

    assert blockchain.chain[-1].data == data

@pytest.fixture
def blockchainThreeBlocks():
    blockchain = Blockchain()
    for i in range(3):
        blockchain.addBlock(i)
    
    return blockchain

def test_isValidChain(blockchainThreeBlocks):
    Blockchain.isValidChain(blockchainThreeBlocks.chain)

def test_isValidChain_chainWithBadSeed (blockchainThreeBlocks):
    blockchainThreeBlocks.chain[0].hash = 'BAD  Hash'

    with pytest.raises (Exception, match = 'Invalid Seed block.'):
        Blockchain.isValidChain(blockchainThreeBlocks.chain)

def test_replaceChain(blockchainThreeBlocks):
    blockchain = Blockchain()
    blockchain.replaceChain(blockchainThreeBlocks.chain)

    assert blockchain.chain == blockchainThreeBlocks.chain

def test_replaceChain_ChainShorter(blockchainThreeBlocks):
    blockchain = Blockchain()

    with pytest.raises(Exception, match = 'Will NOT replace. Incoming chain must be longer than local chain.'):
        blockchainThreeBlocks.replaceChain(blockchain.chain)

def test_replaceChain_badChain(blockchainThreeBlocks):
    blockchain = Blockchain()
    blockchainThreeBlocks.chain[1].hash = 'BAD Hash'
    with pytest.raises(Exception, match = 'Will NOT replace. Invalid incoming chain'):
        blockchain.replaceChain(blockchainThreeBlocks.chain)



