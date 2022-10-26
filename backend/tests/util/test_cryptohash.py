from backend.util.cryptohash import cryptoHash

def test_cryptoHash():
    # Creates the same hash for arguments of different types in any order
    assert cryptoHash(1, [2], 'three') == cryptoHash('three', 1, [2])
    assert cryptoHash('foo') == '7822850fecc31ad84d42bc4dfad785dc1ba286202e19271979763f9c39aba48156a3374d8f483b0a7f0dd5d1b044d4452fba5d8495501f7bcf526db1ad1691f3'