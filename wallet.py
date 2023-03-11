import json
import os

from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import serialization
from blockchain import DodoCoin

# Provides an interface to a user to participate in Dodocoin network
# It provides private and public keys to a user.
dodo = DodoCoin()
users_wallets = {}

class Wallet:
    # Problem Statement 1.a
    # Add a new default parameter generate_key
    def __init__(self, user, node, balance=20):
        self.user = user
        self.__private_key = ''
        self.public_key = ''
        self.associated_node = node  # New attribute. Set during wallet creation. Or explicitly associated with a node
        self.balance = balance  # New attribute. Shows number of coins available in wallet.
        # 20 coins will be given to each user at the time of wallet creation.

        # Problem Statement 1.a: Add new protected instance variable _generate_key
        key_loc_path = self.user + "_private_key.pem"
        check_key = os.path.exists(key_loc_path)
        if check_key:
            self._generate_key = False
        else:
            self._generate_key = True
        users_wallets[self.user] = self
        self.__generate_keys()

    def __generate_keys(self):
        # Problem Statement 1.a.i
        # Check if the _generate_key is True or not
        if self._generate_key:
            self.__private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
            self.public_key = self.__private_key.public_key()

        else:
            print("Keys already exist for this user. Loading existing keys... ")
            # Load existing keys for the user.
            if (isinstance(self.__private_key, rsa.RSAPrivateKey)) is False:
                self.deserialize_private_key()
            else:
                pass

            if (isinstance(self.public_key, rsa.RSAPublicKey)) is False:
                self.deserialize_public_key()
                dodo.register_wallet(self.user, self.public_key)
            else:
                pass

    def create_transaction(self, receiver, coins):
        transaction = {'sender': self.user, "receiver": receiver, "coins": coins}
        # This part digitally signs a transaction.
        # This has the following steps

        # 1. We convert the dictionary which contains transaction details to a string
        # For this we convert this to a JSON string.
        transaction_jsonified = json.dumps(transaction)

        # 2. Change this string to a byte stream. Call the function encode() to encode the string in utf-8 format
        transaction_jsonified_to_bytes = transaction_jsonified.encode()

        # 3. Digitally sign the transaction
        signature = self.__private_key.sign(transaction_jsonified_to_bytes,
                                            padding.PSS(mgf=padding.MGF1(hashes.SHA256()),
                                                        salt_length=padding.PSS.MAX_LENGTH),
                                            hashes.SHA256())

        # 4. Structure the information and pass is back to the caller.
        # This structure will be passed to node for verification.
        # On successful verification, this transaction will be added to the mem_pool
        # a. Sender details. We will use this to pick the public key of sender and validate the transaction
        # b. Signature. Of the transaction
        # c. transaction. Now we are sending encrypted message
        new_transaction = {'sender': self.user,
                           "signature": signature,
                           "transaction_bytes": transaction_jsonified_to_bytes}
        return new_transaction

    def initiate_transaction(self, receiver, coins):
        # Problem Statement 1.b
        # Check whether __private_key is valid or not
        print(f"\nTransaction initiated for sending {coins} coins from {self.user} to {receiver}. ")
        if (isinstance(self.__private_key, rsa.RSAPrivateKey)) is False:
            self.deserialize_private_key()
        else:
            pass

        # Check whether __private_key is valid or not
        if (isinstance(self.public_key, rsa.RSAPublicKey)) is False:
            self.deserialize_public_key()
            dodo.register_wallet(self.user, self.public_key)
        else:
            pass

        # Check whether enough coin balance is available in sender's wallet
        if self.balance >= coins:
            # self.balance = self.balance - coins
            # rcvr_wallet = users_wallets[receiver]
            # rcvr_wallet.balance = rcvr_wallet.balance + coins
            new_transaction = self.create_transaction(receiver, coins)
            # self.show_balance()
            # rcvr_wallet.show_balance()

            # The created transaction will be passed to the associated node for validation.
            if self.associated_node:
                self.associated_node.add_new_transaction(new_transaction)
            else:
                print(f"No node is associated with user {self}.")
        else:
            print(f"Error : User {self.user} does not have enough balance to do this transaction.")
            self.show_balance()
            response = input("Do you want to add balance to this account? Type Y or N. \n")
            if response in ["Y", "y", "yes", "YES", "Yes"]:
                print("Noted. 50 coins will be added to this account.")
                self.make_me_rich()
                self.initiate_transaction(receiver, coins)
            elif response in ["N", "n", "no", "NO", "No"]:
                print("Noted. Transaction cancelled.")
            else:
                print("Invalid response. Only Y or N are accepted.")
                print("Transaction cancelled.")


    def serialize_private_key(self):
        private_key_pem = self.__private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                           format=serialization.PrivateFormat.PKCS8,
                                                           encryption_algorithm=serialization.NoEncryption())

        filename = self.user + "_private_key.pem"
        with open(filename, 'wb') as fhandle:
            fhandle.write(private_key_pem)

    def serialize_public_key(self):
        public_key_pem = self.public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                      format=serialization.PublicFormat.SubjectPublicKeyInfo)
        filename = self.user + "_public_key.pem"
        with open(filename, 'wb') as fhandle:
            fhandle.write(public_key_pem)

    def deserialize_private_key(self):
        filename = self.user + "_private_key.pem"
        with open(filename, "rb") as key_file:
            # Problem Statement 1.a.iii
            # Change the code below to initialise the private instance variable __private_key
            self.__private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )

    def deserialize_public_key(self):
        filename = self.user + "_public_key.pem"
        with open(filename, "rb") as key_file:
            # Problem Statement 1.a.iv
            # Change the code below to initialise the public instance variable public_key
            self.public_key = serialization.load_pem_public_key(
                key_file.read()
            )

    # Problem Statement 1.c.i
    # The function will accept a parameter “filename”
    # Use this filename to serialize the private key
    def serialize_private_key_to_file(self, filename):
        # Problem Statement 1.c.i
        private_key_pem = self.__private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                           format=serialization.PrivateFormat.PKCS8,
                                                           encryption_algorithm=serialization.NoEncryption())
        with open(filename, 'wb') as fhandle:
            fhandle.write(private_key_pem)
        print(f"{self.user}'s private key is serialized to {filename}")

    # The function will accept a parameter “filename”
    # Use this filename to deserialize the private key
    def deserialize_private_key_from_file(self, filename):
        # Problem Statement 1.c.ii
        with open(filename, "rb") as key_file:
            self.__private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
            )
        print(f"{self.user}'s private key is deserialized from {filename}")

    # The function will accept a parameter “filename”
    # Use this filename to serialize the public key
    def serialize_public_key_to_file(self, filename):
        public_key_pem = self.public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                      format=serialization.PublicFormat.SubjectPublicKeyInfo)
        with open(filename, 'wb') as fhandle:
            fhandle.write(public_key_pem)
        print(f"{self.user}'s public key is serialized to {filename}")

    # Problem Statement 1.c.ii
    # The function will accept a parameter “filename”.
    # Use this filename to deserialize the public key
    def deserialize_public_key_from_file(self, filename):
        with open(filename, "rb") as key_file:
            self.public_key = serialization.load_pem_public_key(
                key_file.read()
            )
        print(f"{self.user}'s public key is deserialized from {filename}")

    def associate_with_node(self, node):
        self.associated_node = node

    # This function displays user balance
    def show_balance(self):
        print(f"Balance for user {self.user} is {self.balance} coins.")

    # This function will add 50 coins to user's wallet.
    def make_me_rich(self):
        self.balance = self.balance + 50
        self.show_balance()


if __name__ == "__main__":
    from blockchain import DodoCoin
    from node import Node

    dodo = DodoCoin()
    node_1 = Node("Node_1", dodo)
    user_set = set()

    # Problem Statement 1.a 
    # Argument generate_key can be added 
    sunil_wallet = Wallet('sunil', node_1)
    harsh_wallet = Wallet('harsh', node_1)
    dodo.register_wallet(sunil_wallet.user, sunil_wallet.public_key)
    dodo.register_wallet(harsh_wallet.user, harsh_wallet.public_key)

    sunil_wallet.initiate_transaction("harsh", 50)
    sunil_wallet.initiate_transaction("harsh", 20)
    dodo.list_pending_transactions()

    sunil_wallet.serialize_private_key()
    sunil_wallet.serialize_public_key()
    harsh_wallet.serialize_private_key()
    harsh_wallet.serialize_public_key()

    sunil_wallet.deserialize_private_key()
    sunil_wallet.deserialize_public_key()
    harsh_wallet.deserialize_private_key()
    harsh_wallet.deserialize_public_key()

    sunil_wallet.serialize_private_key_to_file("new_sunil_prk.pem")
    sunil_wallet.serialize_public_key_to_file("new_sunil_pbk.pem")
    harsh_wallet.serialize_private_key_to_file("new_harsh_prk.pem")
    harsh_wallet.serialize_public_key_to_file("new_harsh_pbk.pem")

    sunil_wallet.deserialize_private_key_from_file("new_sunil_prk.pem")
    sunil_wallet.deserialize_public_key_from_file("new_sunil_pbk.pem")
    harsh_wallet.deserialize_private_key_from_file("new_harsh_prk.pem")
    harsh_wallet.deserialize_public_key_from_file("new_harsh_pbk.pem")
