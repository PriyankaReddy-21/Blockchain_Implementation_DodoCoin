from blockchain import DodoCoin
from wallet import Wallet
from node import Node, create_node

dodo = DodoCoin()

# Create nodes
node_1 = create_node("Node-1", dodo)
node_2 = create_node("Node-2", dodo, node_1)
node_3 = create_node("Node-3", dodo, node_2)
node_4 = create_node("Node-4", dodo, node_3)
node_5 = create_node("Node-5", dodo, node_4)
node_6 = create_node("Node-6", dodo, node_5)

# Create users & wallets
peter_wallet = Wallet('Peter', node_1)
tony_wallet = Wallet('Tony', node_1)
strange_wallet = Wallet('Strange', node_2)
bruce_wallet = Wallet('Bruce', node_2)
steve_wallet = Wallet('Steve', node_3)
carol_wallet = Wallet('Carol', node_3)
scarlet_wallet = Wallet('Scarlet', node_4)
nebula_wallet = Wallet('Nebula', node_4)
natasha_wallet = Wallet("Natasha", node_5)
shuri_wallet = Wallet('Shuri', node_5)

# Register each wallet with Blockchain
dodo.register_wallet(peter_wallet.user, peter_wallet.public_key)
dodo.register_wallet(tony_wallet.user, tony_wallet.public_key)
dodo.register_wallet(strange_wallet.user, strange_wallet.public_key)
dodo.register_wallet(bruce_wallet.user, bruce_wallet.public_key)
dodo.register_wallet(steve_wallet.user, steve_wallet.public_key)
dodo.register_wallet(carol_wallet.user, carol_wallet.public_key)
dodo.register_wallet(scarlet_wallet.user, scarlet_wallet.public_key)
dodo.register_wallet(nebula_wallet.user, nebula_wallet.public_key)
dodo.register_wallet(natasha_wallet.user, natasha_wallet.public_key)
dodo.register_wallet(shuri_wallet.user, shuri_wallet.public_key)

# Show list of registered wallets.
print("\n********************************************************************************")
print("\nList of registered wallets.")
dodo.list_wallets()

# Show all nodes
print("\n********************************************************************************")
print(f"{node_1}")
node_1.show_connected_nodes()
print(f"{node_2}")
node_2.show_connected_nodes()
print(f"{node_3}")
node_3.show_connected_nodes()
print(f"{node_4}")
node_4.show_connected_nodes()
print(f"{node_5}")
node_5.show_connected_nodes()
print(f"{node_6}")
node_6.show_connected_nodes()

# Transaction - 1
print("\n\n********************************************************************************\n")
print("Transaction - 1\n")
transaction = peter_wallet.initiate_transaction(tony_wallet.user, 20)
print("List of pending transactions:")
dodo.list_pending_transactions()

# Block index will become 1
node_1.create_new_block()

# node_1.show_chain()
# node_2.show_chain()
# node_3.show_chain()
# node_4.show_chain()
# node_5.show_chain()
# node_6.show_chain()

# Transaction - 2
print("\n********************************************************************************\n")
print("Transaction - 2")
peter_wallet.initiate_transaction(bruce_wallet.user, 25)
bruce_wallet.initiate_transaction(peter_wallet.user, 50)
tony_wallet.initiate_transaction(bruce_wallet.user, 50)
print("List of pending transactions:")
dodo.list_pending_transactions()

# Block index will become 2
node_1.create_new_block()

# node_1.show_chain()
# node_2.show_chain()
# node_3.show_chain()
# node_4.show_chain()
# node_5.show_chain()
# node_6.show_chain()

# Transaction - 3
print("\n********************************************************************************\n")
print("Transaction - 3")
scarlet_wallet.initiate_transaction(peter_wallet.user, 25)
carol_wallet.initiate_transaction(steve_wallet.user, 50)
steve_wallet.initiate_transaction(bruce_wallet.user, 50)
print("List of pending transactions:")
dodo.list_pending_transactions()

# Block index will become 3
node_2.create_new_block()

# print("\nPrinting blockchain for Node - 1")
# print(node_1)
# print("\nPrinting blockchain for Node - 2")
# print(node_2)
node_1.show_chain()
node_2.show_chain()
node_3.show_chain()
node_4.show_chain()
node_5.show_chain()
node_6.show_chain()
print("\n")

# Make new node connections and print all connected nodes
print("\n********************************************************************************")
print("\nMake new node connections and print all connected nodes: ")
print("\nNode 2 is now connected to Node 4 also.")
node_2.connect_with_new_node(node_4, True)
node_1.show_connected_nodes()
node_2.show_connected_nodes()
node_3.show_connected_nodes()
node_4.show_connected_nodes()
node_5.show_connected_nodes()
node_6.show_connected_nodes()
print("\n")

# Add new nodes & try to add duplicate nodes
print("\n********************************************************************************")
node_4 = create_node("Node-4", dodo, node_1)  # duplicate node
node_7 = create_node("Node-7", dodo, node_6)  # new node
node_1.show_connected_nodes()
# node_2.show_connected_nodes()
# node_3.show_connected_nodes()
node_4.show_connected_nodes()
# node_5.show_connected_nodes()
node_6.show_connected_nodes()
node_7.show_connected_nodes()
node_7.show_chain()
print("\n")
