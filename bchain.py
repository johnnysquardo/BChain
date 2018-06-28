import functools
import hashlib
from collections import OrderedDict

import hash_util

# Initializing our blockchain list

MINING_REWARD = 10

genesis_block = {
        'previous_hash': '',
        'index': 0,
        'transactions': [],
        'proof': 100
    }
blockchain = [genesis_block]
open_transactions = []
owner = 'Johnny'

participants= {'Johnny'}


def valid_proof(transactions, last_hash, proof):
    guess = (str(transactions) + str(last_hash) + str(proof)).encode()
    guess_hash = hash_string_256(guess)
    print(guess_hash)
    return guess_hash[0:2] == '00'

def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    while not valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def get_balance(participant):
    tx_sender = [[tx['amount'] for tx in block['transactions'] if tx['sender'] == participant] for block in blockchain]
    open_tx_sender = [tx['amount'] for tx in open_transactions if tx['sender'] == participant]
    tx_sender.append(open_tx_sender)
    print(tx_sender)
    amount_sent = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_sender, 0)
    tx_recipient = [[tx['amount'] for tx in block['transactions'] if tx['recipient'] == participant] for block in blockchain]
    amount_recieved = functools.reduce(lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0, tx_recipient, 0)
    #Return total balance
    return amount_recieved - amount_sent

# This gets the last value of the current blockchain
def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

def verify_transaction(transaction):
    sender_balance = get_balance(transaction['sender'])
    return sender_balance >= transaction['amount']
    
    

# Adds a new value and also grabs the last blockchain value
def add_transaction(recipient, sender=owner, amount=1.0):
    """ Append a new value as well as the last blockchain value """
    # transaction = {
    #     'sender': sender,
    #     'recipient': recipient,
    #     'amount': amount
    # }
    transaction = OrderedDict(
        [('sender', sender), ('recipient', recipient), ('amount', amount)])
    if verify_transaction(transaction):    
        open_transactions.append(transaction)
        participants.add(sender)
        participants.add(recipient)
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
    reward_transaction = OrderedDict([('sender', 'MINING'), ('recipient', owner), ('amount', MINING_REWARD)])
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = {
        'previous_hash': hashed_block,
        'index': len(blockchain),
        'transactions': copied_transactions,
        'proof': proof
    }    
    blockchain.append(block)
    return True

# Gets the transaction value
def get_transaction_value():
    tx_recipient = input('Enter the recipient of the transaction: ')
    tx_amount = float(input('Your transaction amount please: '))
    return tx_recipient, tx_amount

# Gets your input
def get_user_choice(): 
    user_input = input('Your choice: ')
    return user_input


def print_blockchain_elements():
    for block in blockchain: 
        print('Outputting Block')
        print(block)
    else:
        print('-' * 20)

def verify_chain():
    for (index, block) in enumerate(blockchain):
        if index == 0:
            continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
            return False
        if not valid_proof(block['transactions'][:-1], block['previous_hash'], block['proof']):
            print('Proof of work is invalid')
            return False
    return True

def verify_transactions():
    return all([verify_transaction(tx) for tx in open_transactions])
  

    
waiting_for_input = True


while waiting_for_input:
    print('Please Choose')
    print('1: Add a new transaction value')
    print('2: Mine a new block')
    print('3: Output the blockchain blocks')
    print('4: Output Participants')
    print('5: Check Transaction validity')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        # Add the transaction amount to the blockchain
        if add_transaction(recipient, amount=amount):
            print('Added Transaction!')
        else:
            print('Transaction Failed!')
        print(open_transactions)
    elif user_choice == '2': 
        mine_block()
        open_transactions = []
    elif user_choice == '3':
        print_blockchain_elements()
    elif user_choice == '4':
        print(participants)
    elif user_choice == '5':
        if verify_transactions():
            print('All transactions are valid')
        else:
            print('There are invalid transactions')

    elif user_choice == 'h':
        # Make sure that you don't try to hack the blockchain if it's empty
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transactions': [{'sender': 'Chris', 'recipient': 'Johnny', 'amount': 100.0}]
            }
    elif user_choice == 'q':
        # This will lead to the loop to exist because it's running condition
        waiting_for_input = False
    else:
        print('Input was invalid. Pease pick a value from the list!')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        break
    print('Balance of {}: {:6.2f}'.format('Johnny', get_balance('Johnny')))
else: 
    print('User Left!')

print('Done!')