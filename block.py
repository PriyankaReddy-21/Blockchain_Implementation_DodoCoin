import time
import hashlib
import json


class Block:
    # Problem Statement 3.b.iii
    # Add a parameter version
    def __init__(self, index, transactions, previous_block_hash, version, difficulty_level=1, metadata=''):
        self._index = index

        # Problem Statement 3.b.iii
        # Create an instance attribute _version
        self.version = version
        self._timestamp = time.time()
        self._previous_block_hash = previous_block_hash
        self._metadata = metadata
        self._merkle_root = ''
        self._nonce = 0
        self._difficulty_level = difficulty_level
        self._block_hash = ''
        self._transactions = transactions
        self._transaction_counter = len(transactions)

        # Problem Statement 3.a.i
        # Create an instance variable _transaction_counter which is set to the length of the transactions list

    def __str__(self):
        return f'\nBlock index: {self._index}' \
               f'\nTimestamp: {self._timestamp}' \
               f'\nPrevious Block Hash: {self._previous_block_hash}' \
               f'\nMetadata: {self._metadata}' \
               f'\nmerkle root: {self._merkle_root}' \
               f'\nNonce: {self._nonce}' \
               f'\nDifficulty level: {self._difficulty_level}' \
               f'\nBlock Hash: {self._block_hash}' \
               f'\nTransactions: {self._transactions}' \
               f'\nTransaction counter: {self._transaction_counter}' \
               f'\nVersion: {self.version}'

        # Problem Statement 3.b.iii
        # Add _version

        # Problem Statement 3.a.i
        # Add _transaction_counter

    def __repr__(self):
        return self.__str__()

    @property
    def block_hash(self):
        return self._block_hash

    @property
    def get_previous_block_hash(self):
        return self._previous_block_hash

    @property
    def get_transactions(self):
        return self._transactions

    @property
    def get_transaction_counter(self):
        return self._transaction_counter

    # Now this function generates hash based on the difficulty level of block.
    # Problem Statement 2.a
    # Change this function so that it returns the hash_value
    def generate_hash(self):
        self._merkle_root = self._generate_merkle_root()
        while True:  # Keep generating a new hash value
            hash_string = ''.join([
                str(self._index),
                str(self._timestamp),
                str(self._previous_block_hash),
                str(self._metadata),
                str(self._merkle_root),
                str(self._nonce),
                str(self._difficulty_level),
                str(self._transactions),
                str(self._transaction_counter),
                str(self.version)
                # Problem Statement 3(c)
                # Add version
                # Add _transaction_counter

            ])
            encoded_hash_string = hash_string.encode('utf-8')
            hash_value = hashlib.sha256(encoded_hash_string).hexdigest()
            if int(hash_value[:self._difficulty_level], 16) == 0:  # Check for difficulty level.
                break
            self._nonce += 1
        self._block_hash = hash_value
        return self._block_hash

    def _generate_merkle_root(self):
        hash_list = self._create_hash_list(self._transactions)
        return self._create_merkle(hash_list, self._transactions)

    def _create_hash_list(self, transactions):
        new_hash_list = []
        for transaction in transactions:
            transaction_jsonified = json.dumps(transaction)
            x = hashlib.sha256(transaction_jsonified.encode()).hexdigest()
            new_hash_list.append(x)

        return new_hash_list

    def _create_merkle(self, hash_list, transactions):
        if not hash_list:
            print("No transactions. Genesis block. No Merkle root.")
            return None

        if len(hash_list) == 1:
            return hash_list[0]

        while len(hash_list) > 1:
            new_hash_list = []
            # new_transactions_list = []
            # Make number of entries even in the list
            if len(hash_list) % 2 != 0:
                hash_list.append(hash_list[-1])
                # transactions.append(transactions[-1])

            counter = 0
            for index in range(0, len(hash_list), 2):
                # concatenated_transactions = transactions[index] + "+" + transactions[index + 1]
                # new_transactions_list.append(concatenated_transactions)

                concatenated_hash = hash_list[index] + hash_list[index + 1]
                new_hash_list.append(hashlib.sha256(concatenated_hash.encode()).hexdigest())
                # print(f"{new_transactions_list[counter]} - {new_hash_list[counter]}")
                counter += 1

            hash_list = new_hash_list
            # transactions = new_transactions_list
            # print()

        return hash_list[0]


if __name__ == "__main__":
    previous_block_hash = hashlib.sha256(b"Previous Block Hash").hexdigest()
    transactions = ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"]
    new_block = Block(index=10, transactions=transactions, previous_block_hash=previous_block_hash,
                      difficulty_level=5, version=None)
    block_hash = new_block.generate_hash()
    print(new_block)
    print(f"Block hash = {block_hash}")
