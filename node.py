from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidSignature
import json

from block import Block
from wallet import users_wallets

total_nodes_dict = {}


# function to check and avoid duplicate nodes / instances.
def create_node(name, dodocoin, connected_node=None):
    if name in total_nodes_dict:
        print(f"{name} already exists, re-assignment not possible.")
        return total_nodes_dict[name]
    else:
        return Node(name, dodocoin, connected_node)


class Node:
    def __init__(self, name, dodocoin, connected_node=None):
        total_nodes_dict[name] = self
        self.node_name = name
        self.cryptocurrency = dodocoin
        self._chain = []
        # Problem Statement 4.a
        # Initialize the attribute connected_nodes as a blank list
        self.connected_nodes = []
        self._get_chain()
        if connected_node is not None:
            connected_node.connect_with_new_node(self)
        else:
            pass

    def __str__(self):
        return f'\n\n{self.node_name} - Chain:\n{self._chain}'

    def _get_chain(self, connected_node=None):
        # Problem Statement 4.b
        # Change the if statement to check for the length of connected_nodes
        if len(self.connected_nodes) == 0:
            if self.cryptocurrency.genesis_block is not None:
                self._chain.append(self.cryptocurrency.genesis_block)
        else:
            self._pull_chain_from_a_node(self.connected_nodes[0])

    def _pull_chain_from_a_node(self, node):
        if node != self:
            self._chain = []
            for chain_block in node._chain:
                self._chain.append(chain_block)
        else:
            pass

    def connect_with_new_node(self, node, sync_chain=True):
        self_node = self
        new_node = node
        # Problem Statement 4.c
        # Change the code to check for length and remove the unwanted code
        # if len(self.connected_nodes) == 0:
        #     self.connected_nodes.pop(0)
        if node not in self.connected_nodes:
            self_node.connected_nodes.append(new_node)
            new_node.connected_nodes.append(self_node)
            if sync_chain is True:
                node_with_longest_chain = self._check_node_with_longest_chain()
                self._pull_chain_from_a_node(node_with_longest_chain)
                new_node._pull_chain_from_a_node(node_with_longest_chain)
            else:
                pass
        else:
            pass

    def _check_node_with_longest_chain(self):
        node_with_longest_chain = None
        for node in self.connected_nodes:
            if len(node._chain) > len(self._chain):
                self._pull_chain_from_a_node(node)
                node_with_longest_chain = self
            else:
                node_with_longest_chain = self
        return node_with_longest_chain

    def create_new_block(self):
        # Problem Statement 3.b.iv
        # Pass an argument current version to the block class
        print(f"\nCreating new block in {self.node_name}...")
        new_block = Block(index=len(self._chain), transactions=self.cryptocurrency.mem_pool,
                          difficulty_level=self.cryptocurrency.difficulty_level,
                          previous_block_hash=self._chain[-1].block_hash, metadata='',
                          version=self.cryptocurrency.current_version)

        new_block.generate_hash()
        flag = self.validate_block(new_block)
        if flag is True:
            self._chain.append(new_block)
            self.cryptocurrency.mem_pool = []
            tx_cntr = new_block.get_transaction_counter
            tx = new_block.get_transactions
            print("New block created successfully!")
            if tx_cntr > 0:
                for item in tx:
                    sender_wallet = users_wallets[item["sender"]]
                    receiver_wallet = users_wallets[item["receiver"]]
                    sender_wallet.balance = sender_wallet.balance - item["coins"]
                    receiver_wallet.balance = receiver_wallet.balance + item["coins"]
                    print(f"\nTransaction {tx.index(item)+1} completed.")
                    print("Displaying account balances of sender and receiver: ")
                    print("Sender:")
                    sender_wallet.show_balance()
                    print("Receiver:")
                    receiver_wallet.show_balance()

            else:
                pass
            # Problem Statement 4.d
            # Change the code to check for length and remove the unwanted code
            if len(self.connected_nodes) != 0:
                self.propagate_new_block_to_connected_nodes(new_block)
            else:
                pass
        else:
            print("Could not create new block.")
        return new_block

    def show_chain(self):
        print(f"\nChain of node - {self.node_name}")
        for chain_block in self._chain:
            print(chain_block)

    def add_new_transaction(self, transaction):
        try:
            self._validate_digital_signature(transaction)
        except InvalidSignature as e:
            print("Invalid signature. Cannot add this transaction")
            return

        if self._validate_receiver(transaction):
            transaction_bytes = transaction['transaction_bytes']
            transaction_data = json.loads(transaction_bytes)
            self.cryptocurrency.mem_pool.append(transaction_data)

    def _validate_digital_signature(self, transaction):
        sender_public_key = self.cryptocurrency.wallets[transaction['sender']]
        signature = transaction['signature']
        transaction_bytes = transaction['transaction_bytes']
        sender_public_key.verify(signature, transaction_bytes,
                                 padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
                                 hashes.SHA256())

    def _validate_receiver(self, transaction):
        transaction_bytes = transaction['transaction_bytes']
        transaction_data = json.loads(transaction_bytes)
        # print(transaction_data)
        if transaction_data['receiver'] in self.cryptocurrency.wallets:
            return True
        return False

    def propagate_new_block_to_connected_nodes(self, new_block):
        for node in self.connected_nodes:
            node.add_new_block(new_block)
        # print(f"Total nodes are: {total_nodes_dict}")
        for item in total_nodes_dict.values():
            node_with_longest_chain = item._check_node_with_longest_chain()
            item._pull_chain_from_a_node(node_with_longest_chain)

    def add_new_block(self, node):
        self._chain.append(node)

    def show_connected_nodes(self):
        # Problem Statement 4.d
        # Change the code to check for length and remove the unwanted code
        if len(self.connected_nodes) != 0:
            print(f"\n{self.node_name} is connected with - ", end="")
            for _node in self.connected_nodes:
                print(_node.node_name, end=", ")
        else:
            print(f"\n{self.node_name} has no connected nodes.")

    # Problem Statement 2.a
    # Function to validate a block before it is propagated through the chain
    # Compare the hash of the last block of this chain against the previous_hash of the new block
    def validate_block(self, new_block):
        flag = None
        index = int(len(self._chain))
        last_block = self._chain[index - 1]
        if last_block.block_hash == new_block.get_previous_block_hash:
            print("\nNew block is valid")
            flag = True
        else:
            print("\nInvalid Block")
            flag = False
        return flag


if __name__ == "__main__":
    from blockchain import DodoCoin
    from wallet import Wallet

    dodo = DodoCoin()
    node_1 = create_node("Node_1", dodo)

    sunil_wallet = Wallet('sunil', node_1)
    harsh_wallet = Wallet('harsh', node_1)
    dodo.register_wallet(sunil_wallet.user, sunil_wallet.public_key)
    dodo.register_wallet(harsh_wallet.user, harsh_wallet.public_key)

    sunil_wallet.initiate_transaction("harsh", 50)
    sunil_wallet.initiate_transaction("harsh", 20)

    node_1.create_new_block()
    node_1.show_chain()

    node_2 = Node("Node_2", dodo, node_1)
    node_2.show_chain()

    dodo.update_difficulty_level(6)

    harsh_wallet.initiate_transaction("sunil", 50)
    harsh_wallet.initiate_transaction("sunil", 20)

    node_1.create_new_block()
    node_1.show_chain()
    node_2.show_chain()
