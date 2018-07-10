import functools
import hashlib
import json
import pickle


from hash_util import hash_block
from block import Block
from transaction import Transaction
from verification import Verification

# Initializing our blockchain list

MINING_REWARD = 10

blockchain = []
open_transactions = []
owner = 'Johnny'


def load_data():
    global blockchain
    global open_transactions
    try:
        with open('blockchain.txt', mode='r') as f:
            # file_content = pickle.loads(f.read())
            file_content = f.readlines()
            # blockchain = file_content['chain']
            # open_transactions = file_content['ot']
            blockchain = json.loads(file_content[0][:-1])
            updated_blockchain = []
            for block in blockchain:
                converted_tx = [Transaction(tx['sender'], tx['recipient'], tx['amount']) for tx in block['transactions']]        
                updated_block = Block(block['index'], block['previous_hash'], converted_tx, block['proof'], block['timestamp'])       
                updated_blockchain.append(updated_block)
            blockchain = updated_blockchain
            open_transactions = json.loads(file_content[1])
            updated_transactions = []
            for tx in open_transactions:
                updated_transaction = Transaction(tx['sender'], tx['recipient'], tx['amount'])
                updated_transactions.append(updated_transaction)
            open_transactions = updated_transactions
    except (IOError, IndexError):
        genesis_block = Block(0, '', [], 100, 0)
        blockchain = [genesis_block]
        open_transactions = []
    finally:
        print('Cleanup!')

    


load_data()
        

def save_data():
    try:
        with open('blockchain.txt', mode='w') as f:
            saveable_chain = [block.__dict__ for block in [Block(block_el.index, block_el.previous_hash, [tx.__dict__ for tx in block_el.transactions], block_el.proof, block_el.timestamp) for block_el in blockchain]]
            f.write(json.dumps(saveable_chain))
            f.write('\n')
            saveable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_tx))
            # save_data = {
            #     'chain': blockchain,
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(save_data))
    except IOError:
        print('Saving failed!')
        

def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    verifier = Verification()
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    tx_sender = [[tx.amount for tx in block.transactions
                  if tx.sender == participant] for block in blockchain]
    open_tx_sender = [tx.amount 
                      for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    print(tx_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    tx_recipient = [[tx.amount for tx in block.transactions
                     if tx.recipient == participant] for block in blockchain]
    amount_recieved = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) 
                             if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    #Return total balance
    return amount_recieved - amount_sent

# This gets the last value of the current blockchain
def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]



# Adds a new value and also grabs the last blockchain value
def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new value as well as the last blockchain value """
    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount
    # }
    transaction = Transaction(sender, recipient, amount)
    verifier = Verification()
    if verifier.verify_transaction(transaction, get_balance):    
        open_transactions.append(transaction)
        save_data()
        return True
    return False
    

def mine_block(): 
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD
    # }
    reward_transaction = Transaction('MINING', owner, MINING_REWARD)
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof) 
    blockchain.append(block)
    return True



    
