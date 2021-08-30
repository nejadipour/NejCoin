import json
import sys
from hashlib import sha256
from time import time
from uuid import uuid4
from flask import Flask, jsonify, request


class BlockChain:
    def __init__(self):
        self.chain = []
        self.current_trxs = []
        self.new_block(100, 1)

    def new_block(self, proof, previous_hash=None):
        """create a new block"""
        block = {
            "index": len(self.chain),
            "timestamp": time(),
            "trxs": self.current_trxs,
            "proof": proof,
            "previous_hash": previous_hash or self.hash(self.chain[-1])
        }

        self.chain.append(block)
        self.current_trxs = []

        return block

    def new_trx(self, sender, recipient, amount):
        """add a new trx to the mempool"""
        self.current_trxs.append(
            {
                "sender": sender,
                "recipient": recipient,
                "amount": amount
            }
        )

        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """hash the block"""
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    @property
    def last_block(self):
        """returns the last block"""
        return self.chain[-1]

    @staticmethod
    def valid_proof(nonce, block):
        """checks the hash of the passed nonce and block
        to see it is less than the DL or not"""
        proof = f'{nonce}{json.dumps(block, sort_keys=True).encode()}'.encode()
        proof_hash = sha256(proof).hexdigest()

        return proof_hash[:4] == '0000'

        pass

    def proof_of_work(self, last_block):
        """shows that enough try has been done or not"""
        nonce = 0
        while self.valid_proof(nonce, last_block) is False:
            nonce += 1

        return nonce


app = Flask(__name__)
node_id = str(uuid4())
blockchain = BlockChain()


@app.route('/mine')
def mine():
    """mine a block and after that add it to the blockchain"""
    # find the new nonce by running the proof of work function
    last_block = blockchain.last_block
    proof_of_work = blockchain.proof_of_work(last_block)

    # after finding the nonce we will get a prize
    blockchain.new_trx(
        sender=0,
        recipient=node_id,
        amount=50
    )

    # now we make a new block
    previous_hash = blockchain.hash(last_block)
    new_block = blockchain.new_block(proof_of_work, previous_hash)

    res = {
        'message': "new block made",
        'index': new_block['index'],
        'trxs': new_block['trxs'],
        'proof': new_block['proof'],
        'previous_hash': new_block['previous_hash']

    }

    return jsonify(res), 200


@app.route('/trxs/new', methods=['POST'])
def new_trx():
    """by calling this function, a new trx will be added"""
    passed_data = request.get_json()
    this_block = blockchain.new_trx(
        passed_data["sender"],
        passed_data["recipient"],
        passed_data["amount"]
    )

    response = {'message': f'will be added to block {this_block}'}

    return jsonify(response), 201


@app.route('/chain')
def get_full_chain():
    output = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }

    return jsonify(output), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(sys.argv[1]))
