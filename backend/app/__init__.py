import os
import requests
import random
from flask import Flask, jsonify, request
from backend.blockchain.blockchain import Blockchain
from backend.wallet.wallet import Wallet
from backend.wallet.transaction import Transaction
from backend.wallet.transactionPool import TransactionPool
from backend.pubsub import PubSub

from backend.config import MAIN_SERVR, ROOT_PORT

app = Flask(__name__)
blockchain = Blockchain()
wallet = Wallet()
transactionPool = TransactionPool()
pubsub = PubSub(blockchain, transactionPool)

@app.route('/')
def routeDefault():
    return 'Welcome to the PerXimmon blockckain'

@app.route('/blockchain')
def routeBlockchain():
    return jsonify(blockchain.toJson())

@app.route('/blockchain/mine')
def routeBlockchainMine():
    transactionData = 'stubbed transaction data'
    blockchain.addBlock(transactionData)

    block = blockchain.chain[-1]
    pubsub.broadcastBlock(block)
    
    return jsonify(block.toJson())

@app.route('/wallet/transact', methods=['POST'])
def routeWalletTransact():
    transactionData = request.get_json()
    transaction = transactionPool.existingTransaction(wallet.address)
    if transaction:
        print('TRANSACTION EXISTS')
        transaction.update(wallet, transactionData['recipient'], transactionData['amount'])
    else:
        print('TRANSACTION DOES NOT EXIST')
        transaction = Transaction(wallet, transactionData['recipient'], transactionData['amount'])

    pubsub.broadcastTransaction(transaction)

    return jsonify(transaction.toJson())

PORT = ROOT_PORT

if os.environ.get('PEER') == 'True':
    PORT = random.randint(5001, 30000)

    result = requests.get(f'{MAIN_SERVR}:{ROOT_PORT}/blockchain')
    resutBlockchain = Blockchain.fromJson(result.json())

    try:
        blockchain.replaceChain(resutBlockchain.chain)
        print('\n--Local chain synchronized SUCCESSFULLY')
    except Exception as e:
        print(f'\n-- Synchronization ERROR: {e}')

app.run(port = PORT)