# Initializing our blockchain list
blockchain = []
open_transactions = []
owner = 'Johnny'

# This gets the last value of the current blockchain
def get_last_blockchain_value():
    """ Returns the last value of the current blockchain """
    if len(blockchain) < 1:
        return None
    return blockchain[-1]

# Adds a new value and also grabs the last blockchain value
def add_transaction(sender, recipient, amount=1.0):
    """ Append a new value as well as the last blockchain value """
    transaction = {
        'sender': sender,
        'recipient': recipient,
        'amount': amount
    }
    open_transactions.append(transaction)
    

def mine_block(): 
    pass

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
    # block_index = 0
    is_valid = True
    for block_index in range(len(blockchain)):
        if block_index == 0:
            continue
        elif blockchain[block_index][0] == blockchain[block_index - 1]:
            is_valid = True
        else:
            is_valid = False
            break
    # for block in blockchain:
    #     if block_index == 0:
    #         block_index += 1
    #         continue
    #     elif block[0] == blockchain[block_index - 1]:
    #         is_valid = True
    #     else:
    #         is_valid = False
    #         break
    #     block_index += 1
    return is_valid

    
waiting_for_input = True


while waiting_for_input:
    print('Please Choose')
    print('1: Add a new transaction value')
    print('2: Output the blockchain blocks')
    print('h: Manipulate the chain')
    print('q: Quit')
    user_choice = get_user_choice()
    if user_choice == '1':
        tx_data = get_transaction_value()
        add_transaction(tx_amount, get_last_blockchain_value())
    elif user_choice == '2':
        print_blockchain_elements()
    elif user_choice == 'h':
        if len(blockchain) >= 1:
            blockchain[0] = [2]
    elif user_choice == 'q':
        waiting_for_input = False
    else:
        print('Input was invalid. Pease pick a value from the list!')
    if not verify_chain():
        print_blockchain_elements()
        print('Invalid blockchain!')
        break
else: 
    print('User Left!')

print('Done!')