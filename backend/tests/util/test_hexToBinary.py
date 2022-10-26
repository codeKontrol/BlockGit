from tokenize import Hexnumber
from backend.util.hexToBinary import hexToBinary

def test_hexToBinary():
    originalNumber = 789
    hexNumber = hex(originalNumber)[2:]
    binaryNumber = hexToBinary(hexNumber)

    assert int(binaryNumber, 2) == originalNumber