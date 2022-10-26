import time
import pytest

from backend.blockchain.block import Block, SEED_DATA
from backend.config import MINE_RATE, SECONDS
from backend.util.hexToBinary import hexToBinary

def test_mineBlock():
    previousBlock = Block.seed()
    data = 'test data'
    block = Block.mineBlock(previousBlock, data)

    assert isinstance(block, Block)
    assert block.data == data
    assert block.previousHash == previousBlock.hash
    assert hexToBinary(block.hash)[0:block.difficulty] == '0' * block.difficulty

def test_seed():
    seed = Block.seed()

    assert isinstance(seed, Block)
    for key, value in SEED_DATA.items():
        getattr(seed, key) == value

def test_quicklyMinedBlock():
    previousBlock = Block.mineBlock(Block.seed(), 'foo')
    minedBlock = Block.mineBlock(previousBlock, 'bar')

    assert minedBlock.difficulty == previousBlock.difficulty + 1

def test_slowlyMinedBlock():
    previousBlock = Block.mineBlock(Block.seed(), 'foo')
    time.sleep(MINE_RATE / SECONDS)
    minedBlock = Block.mineBlock(previousBlock, 'bar')

    assert minedBlock.difficulty == previousBlock.difficulty - 1

def test_minedBlockDifficultyLimitsAt1():
    previousBlock = Block(
        1,
        time.time_ns(),
        'testPreviousHash',
        'testHash',
        'testData',
        1,
        0
    )

    time.sleep(MINE_RATE / SECONDS)
    minedBlock = Block.mineBlock(previousBlock, 'bar')

    assert minedBlock.difficulty == 1

@pytest.fixture
def previousBlock():
    return Block.seed()

@pytest.fixture
def block(previousBlock):
    return Block.mineBlock(previousBlock, 'testData')
    
def test_isValidBlock(previousBlock, block):
    Block.isValidBlock(previousBlock, block)

def test_isValidBlock_badPreviousHash(previousBlock, block):
    block.previousHash = 'bad previousHash'
    with pytest.raises(Exception, match = 'PreviousHash is not correct'):
        Block.isValidBlock(previousBlock, block)

def test_isValidBlock_badProofOfWork(previousBlock, block):
    block.hash = 'fff'
    with pytest.raises(Exception, match = 'Proof of work requirement was not met'):
        Block.isValidBlock(previousBlock, block)

def test_isValidBlock_jumpedDifficulty(previousBlock, block):
    jumpedDifficulty = 10
    block.difficulty = jumpedDifficulty
    block.hash = f'{"0" * jumpedDifficulty}111abc'
    with pytest.raises(Exception, match = 'Block difficulty must only be adjusted by 1.'):
        Block.isValidBlock(previousBlock, block)

def test_isValidBlock_badBlockHash(previousBlock, block):
    block.hash = '000000000000000bad1'
    with pytest.raises(Exception, match = 'Block hash is not correct.'):
        Block.isValidBlock(previousBlock, block)

