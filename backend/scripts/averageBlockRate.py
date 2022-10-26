import time

from backend.blockchain.blockchain import Blockchain
from backend.config import SECONDS

blockchain = Blockchain()

times = []

for i in range (1000):
    startTime = time.time_ns()
    blockchain.addBlock(i)
    endTime = time.time_ns()

    timeToMine = (endTime - startTime) / SECONDS
    times.append(timeToMine)

    averageTime = sum(times) / len(times)

    print(f'New block difficulty: {blockchain.chain[-1].difficulty}')
    print(f'Time to mine a new block: {timeToMine} S')
    print(f"Average time to add blocks: {averageTime} S\n")