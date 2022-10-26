from backend.util.cryptohash import cryptoHash

HEX_TO_BINARY_CONVERSION_TABLE = {
    '0': '0000',
    '1': '0001',
    '2': '0010',
    '3': '0011',
    '4': '0100',
    '5': '0101',
    '6': '0110',
    '7': '0111',
    '8': '1000',
    '9': '1001',
    'a': '1010',
    'b': '1011',
    'c': '1100',
    'd': '1101',
    'e': '1110',
    'f': '1111'
}

def hexToBinary (hexString):
    binaryString = ''
    for character in hexString:
        binaryString += HEX_TO_BINARY_CONVERSION_TABLE[character]

    return binaryString

def main():
    number = 451
    hexNumber = hex(number)[2:]
    print(f'hexNumber: {hexNumber}')

    binaryNumber = hexToBinary(hexNumber)
    print(f'binaryNumber: {binaryNumber}')

    originalNumber = int(binaryNumber, 2)
    print(f'originalNumber: {originalNumber}')

    hexToBinaryCryptoHash = hexToBinary(cryptoHash('testData'))
    print(f'hexToBinaryCryptoHash: {hexToBinaryCryptoHash}')



if __name__ == '__main__':
    main()