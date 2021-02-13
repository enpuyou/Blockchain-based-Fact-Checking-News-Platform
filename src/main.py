"""
Node runner for Blockchain, to interact with using HTTP requests.
"""

import argparse

from typing import List
from uuid import uuid4

import uvicorn

from fastapi import FastAPI
from pydantic import BaseModel

try:
    from src.blockchain import Block, BlockChain
except ImportError:
    from blockchain import Block, BlockChain


print("Instantiating node")
node = FastAPI()

print("Generating globally unique address for this node")
NODE_IDENTIFIER = str(uuid4()).replace("-", "")
print(f"This is node ID {NODE_IDENTIFIER}")

print("Instantiating Blockchain for this node")
blockchain = BlockChain()
print("Blockchain up and running!")


class ActiveNode(BaseModel):
    nodes: List[str]


@node.get("/")
def root():
    """
    Greet info
    """
    return {
        "message": "Welcome to the simplified blockchain news platform"
    }


@node.get("/mine")
def mine_block():
    """
    Mining endpoint tha mines current transactions
    """
    print("Received GET request to add a block")
    index = blockchain.mine()

    return {
        "message": "New Block Forged",
        "current index": index
    }


@node.post("/transactions/new")
def new_transaction(new_transaction):
    """
    Receives transaction data from a POST request and add it to blockchain.
    """
    print("Received POST request for new transaction")
    blockchain.add_transaction(new_transaction)

    return {
        "message": "Transaction added and will be mined soon"
    }


@node.get("/chain")
def full_chain():
    """
    GETing `/chain` will returns the full blockchain.

    Returns:
        The node's full blockchain list, as a JSON response.
    """
    print("Received GET request for the full chain")
    return {
        "chain": blockchain.chain.asdict(),
        "length": len(blockchain.chain),
    }


# def _parse_arguments():
#     """Simply parse the port on which to run."""
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "-p",
#         "--port",
#         dest="port",
#         default=5000,
#         type=int,
#         help="The port on which to run a node. Defaults to 5000.",
#     )
#     parser.add_argument(
#         "--host",
#         dest="host",
#         default="127.0.0.1",
#         type=str,
#         help="The host on which to run the node. Defaults to '127.0.0.1', known as 'localhost'.",
#     )
#     return parser.parse_args()
