class BlockChain:
    def __init__(self):
        self.chain = []
        self.current_trxs = []

    def new_block(self):
        """create a new block"""
        pass

    def new_trx(self, sender, recipient, amount):
        """add a new trx to the mempool"""
        pass


    @staticmethod
    def hash(block):
        """hash the block"""
        pass

    @property
    def last_block(self):
        """returns the last block"""
        pass
