import json
from hashlib import sha256
from time import time


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
        pass

    @staticmethod
    def valid_proof(nonce, block):
        """checks the hash of the passed nonce and block
        to see it is less than the DL or not"""
        proof = f'{nonce}{json.dumps(block, sort_keys=True).encode()}'
        proof_hash = sha256(proof).hexdigest()

        return proof_hash[:4] == '0000'

        pass

    def proof_of_work(self):
        """shows that enough try has been done or not"""
        nonce = 0
        while self.valid_proof(nonce, self.chain[-1]) is False:
            nonce += 1

        return nonce
