# ref: https://towardsdatascience.com/building-a-minimal-blockchain-in-python-4f2e9934101d
# ref: https://github.com/edenau/minimal-blockchain/blob/master/main.ipynb

import copy  # fork a chain
from datetime import datetime  # get real time for timestamps
import hashlib  # hash
import statistics
from merklelib import MerkleTree, beautify
try:
    from src.factchecker import retrieve_review
except ImportError:
    from factchecker import retrieve_review
from pprint import pprint
# from urllib.parse import ParseResult, ParseResultBytes, urlparse
# from pydantic import BaseModel


# class Transaction(BaseModel):
#     sender: str
#     recipient: str
#     amount: float


# class Block(BaseModel):
#     index: int
#     timestamp: float
#     transactions: List[Transaction]
#     previous_hash: Optional[int]
#     hash: str

class Block:
    def __init__(self, index, timestamp, transactions, previous_hash, news, nonce=0):
        self.index = index
        self.timestamp = timestamp
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.news = news
        self.nonce = nonce

    def compute_hash(self):
        key = hashlib.sha256()
        key.update(str(self.index).encode("utf-8"))
        key.update(str(self.timestamp).encode("utf-8"))
        key.update(str(self.transactions).encode("utf-8"))
        key.update(str(self.previous_hash).encode("utf-8"))
        key.update(str(self.nonce).encode("utf-8"))
        return key.hexdigest()

    def asdict(self):
        """Return the block as a dictionary"""
        return self.__dict__


class BlockChain:
    difficulty = 3
    previous_article = ""
    article_index = -1

    def __init__(self, chain=None):  # initialize when creating a chain
        self.unconfirmed_transactions = []
        self.chain = []
        if chain is None:
            self.create_genesis_block()
        # self.current_transactions = []

    def create_genesis_block(self):
        """Make a first block"""
        genesis_block = Block(0, str(datetime.utcnow()), "genesis", "", "")
        genesis_block.hash = self.proof_of_work(genesis_block)
        self.chain.append(genesis_block)

    def asdict(self):
        """Return the block as a dictionary"""
        chain_lst = []
        for block in self.chain[1:]:
            chain_lst.append(block.asdict())
        return chain_lst

    @property
    def last_block(self):
        """
        return the last block in the current blockchain
        """
        return self.chain[-1]

    def add_block(self, block, proof):
        """
        Append a block to the current blockchain
        """

        # verify hash
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False

        # verify proof
        if not self.is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        # self.chain.append(block)
        return True

    def is_valid_proof(self, block, block_hash):
        """
        Check if block is valid comparing to the previous block
        """
        is_valid_prefix = block_hash.startswith('0' * self.difficulty)
        if block_hash == block.compute_hash():
            is_same_hash = True
        else:
            is_same_hash = False
        return is_valid_prefix and is_same_hash

    def proof_of_work(self, block):
        """
        proof of work with nonce and return the hash
        """
        block.nonce = 0
        computed_hash = block.compute_hash()
        while not computed_hash.startswith('0' * self.difficulty):
            block.nonce += 1
            computed_hash = block.compute_hash()
        return computed_hash

    def get_chain_size(self):
        """
        return the size of the current chain
        exclude genesis block
        """
        return len(self.chain) - 1

    def add_new_transaction(self, transaction):
        """
        Add a new transaction to the list await for verification
        """
        if isinstance(transaction, str):
            self.unconfirmed_transactions.append({transaction: []})
            self.previous_article = transaction
            self.article_index += 1
        else:
            self.unconfirmed_transactions[
                self.article_index][self.previous_article].append(transaction)

    def mine(self):
        """
        Add pending transactions to the blockchain through proof of work
        """
        if not self.unconfirmed_transactions:
            return False

        article = ""
        for item in self.unconfirmed_transactions:
            article = list(item.keys())[0]
            root_hash, stdev, mean, var = self.make_tree(item[article])

            last_block = self.last_block
            new_block = Block(
                index=last_block.index + 1,
                transactions=root_hash,
                timestamp=str(datetime.utcnow()),
                previous_hash=last_block.hash,
                news={
                    "value": article,
                    "review": retrieve_review(article),
                    "stdev": stdev,
                    "mean": mean,
                    "variance": var
                }
            )

            proof = self.proof_of_work(new_block)
            self.add_block(new_block, proof)

        # reset the unconfirmed transaction
        self.unconfirmed_transactions = []
        self.previous_article = ""
        self.article_index = -1
        return new_block.index

    def fork(self, head="latest"):
        if head in ["latest", "whole", "all"]:
            return copy.deepcopy(self)  # deepcopy since they are mutable
        else:
            c = copy.deepcopy(self)
            c.blocks = c.blocks[0: head + 1]
            return c

    def make_tree(self, transactions):
        """
        Make merkle tree from a list of transactions and return root hash
        """
        tree = MerkleTree(transactions)
        # beautify(tree)
        stdev = self.standard_dev(transactions)
        mean = self.mean(transactions)
        variance = self.variance(transactions)
        return tree.merkle_root, stdev, mean, variance

    def standard_dev(self, lst):
        """
        compute standard deviation
        """
        return statistics.stdev(lst)

    def variance(self, lst):
        """
        compute standard deviation
        """
        return statistics.variance(lst)

    def mean(self, lst):
        """
        compute mean
        """
        return statistics.mean(lst)


if __name__ == '__main__':

    c = BlockChain()  # Start a chain
    import random
    import time
    claims = []
    cmd = input("Enter claim 1:\n")
    claims.append(cmd)
    c.add_new_transaction(cmd)
    for i in range(10):
        random_num = random.randint(0, 3)
        print(f"Randomly generated evaluation: {random_num}")
        time.sleep(1)
        c.add_new_transaction(random_num)
    time.sleep(1.5)
    cmd = input("Enter claim 2:\n")
    claims.append(cmd)
    c.add_new_transaction(cmd)
    for i in range(10):
        random_num = random.randint(6, 10)
        print(f"Randomly generated evaluation: {random_num}")
        time.sleep(1)
        c.add_new_transaction(random_num)
    time.sleep(1.5)
    cmd = input("Enter claim 3:\n")
    claims.append(cmd)
    # print("Claim 3: Healthy people do not need to wear masks")
    c.add_new_transaction(cmd)
    for i in range(10):
        random_num = random.randint(3, 10)
        print(f"Randomly generated evaluation: {random_num}")
        time.sleep(1.5)
        c.add_new_transaction(random_num)
    print("Mining")
    time.sleep(3)
    c.mine()
    print()
    for i, review in enumerate(c.asdict()):
        print(f"Block {i + 1}: {claims[i]}")
        print()
        pprint(review)
        print()
