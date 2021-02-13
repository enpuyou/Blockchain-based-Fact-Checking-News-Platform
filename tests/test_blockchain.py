from src.blockchain import Block, BlockChain
from datetime import datetime


def test_block_compute_hash():
    """test if the block computes the has correctly"""
    block = Block(0, "01-01-2020", "genesis", "", "")
    output = block.compute_hash()
    expected = "d73700745cf9f04132a7e05a79265e870f784c28641f679cc163017517e1ba65"
    assert output == expected


def test_block_return_dict():
    """test that block return as a dict when requested"""
    block = Block(0, "01-01-2020", "genesis", "", "")
    output = block.asdict()
    expected = {
        'index': 0,
        'news': '',
        'nonce': 0,
        'previous_hash': '',
        'timestamp': '01-01-2020',
        'transactions': 'genesis'}
    assert output == expected


def test_blockchain_create_genesis_block():
    """test that blockchain creates the genesis block correctly"""
    blockchain = BlockChain()
    output = blockchain.chain[0].index
    assert output == 0


def test_blockchain_proof_of_work():
    """test proof of work works correctly"""
    block = Block(0, "01-01-2020", "genesis", "", "")
    blockchain = BlockChain()
    output = blockchain.proof_of_work(block=block)
    expected = "00eddca60c19374852bebd291a7ec6baaf3bbeb4bcb4737edca7974150567c3f"
    assert output == expected


def test_blockchain_is_valid_proof():
    """test the valid proof function works correctly"""
    block = Block(0, "01-01-2020", "genesis", "", "")
    blockchain = BlockChain()
    blockchain.proof_of_work(block=block)
    input_hash = "00eddca60c19374852bebd291a7ec6baaf3bbeb4bcb4737edca7974150567c3f"
    output = blockchain.is_valid_proof(block, input_hash)
    assert output is True


def test_blockchain_get_chain_size():
    """test blockchain returns correct chain size"""
    blockchain = BlockChain()
    output = blockchain.get_chain_size()
    assert output == 0


def test_blockchain_as_dict():
    """test the blockchain work flow"""
    blockchain = BlockChain()  # Start a chain
    blockchain.add_new_transaction("claim")
    for i in range(1, 7):
        blockchain.add_new_transaction(i)
    blockchain.mine()
    assert isinstance(blockchain.asdict(), list) is True


def test_blockchain_work_chain_size():
    """test the blockchain work flow"""
    blockchain = BlockChain()  # Start a chain
    blockchain.add_new_transaction("claim")
    for i in range(1, 7):
        blockchain.add_new_transaction(i)
    blockchain.mine()
    assert blockchain.get_chain_size() == 1


def test_blockchain_work_chain():
    """test the blockchain work flow"""
    blockchain = BlockChain()  # Start a chain
    blockchain.add_new_transaction("claim")
    for i in range(1, 7):
        blockchain.add_new_transaction(i)
    blockchain.mine()
    assert blockchain.get_chain_size() == 1
    assert isinstance(blockchain.chain[1].asdict(), dict) is True


def test_blockchain_work_index():
    """test the blockchain work flow"""
    blockchain = BlockChain()  # Start a chain
    blockchain.add_new_transaction("claim")
    for i in range(1, 7):
        blockchain.add_new_transaction(i)
    blockchain.mine()
    assert blockchain.chain[1].index == 1


def test_blockchain_work_mine_result():
    """test the blockchain work flow"""
    blockchain = BlockChain()  # Start a chain
    blockchain.add_new_transaction("claim")
    for i in range(1, 7):
        blockchain.add_new_transaction(i)
    blockchain.mine()
    assert blockchain.chain[1].news["mean"] == 3.5
    assert blockchain.chain[1].news["value"] == "claim"
