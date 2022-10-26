import hashlib
import json


def cryptoHash(*args):
    """
    Returns a sha512 hash of the given arguments.
    """
    stringedArgs = sorted(map(lambda data: json.dumps(data), args))
    joinedData = ''.join(stringedArgs)

    return hashlib.sha512(joinedData.encode('utf-8')).hexdigest()

def main():
    print(f"cryptoHash(2, 'one', [3]): {cryptoHash(2, 'one', [3])}")

if __name__ == '__main__':
    main()