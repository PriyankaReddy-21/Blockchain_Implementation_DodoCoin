
### Blockchain implementation - DodoCoin


#### Introduction 

In this project, I have implemented a blockchain network for DodoCoin. Code structure and project assumptions are given below in detail. Final project results are documented in output folder.



#### Code structure

1. Class Block (Block.py) 
  - This class implements the functionality of a typical block of a blockchain. 
  - This contains header information (index, timestamp, previous block hash, Merkle root, etc.) which is used to generate a hash for this block. 
  - It also contains a list of the transactions that are part of this block. 
  - It implements the functionality of generating both Merkle root and hash of a block with a defined difficulty level. 

2. Class Wallet (Wallet.py) 
  - This class provides an interface for a user to participate in the DodoCoin network. 
  - It provides private and public keys to a user. 
  - A user uses these keys to initiate a transaction on the network. 
  - While creating a new transaction, this class digitally signs a transaction as well. 
  - It also provides the functionality of serializing and deserializing the keys to a default   pre-defined filename.
  - Additional optional functionality is given for serializing and deserializing the keys to a user-defined filename.
  - It also maintains balance of each user. An opening balance of 20 coins is added for user during new wallet creation.

3. Class Node (Node.py) 
  - This class implements the functionality of a Node. 
  - Each node maintains its own list of users and connected nodes. 
  - Each node also maintains its own copy of the complete blockchain. 
  - New nodes are added as defined / created by users & can be connected with existing nodes.
  - When a block is created by any node, it is verified and propagated to all its connected nodes.
  - During block propagation & new node addition / connection, a sync functionality is implemented to ensure all nodes have the longest chain.

4. Class DodoCoin (blockchain.py) 
- This class is the starting point of the blockchain network. 
- When an object is created, it creates the very first “genesis” block. 
- It also provides the functionality of managing the transactions that are yet to be added to a block. 
- It also maintains a list of public keys of all the users of this network. This is done with an intention of explaining the concept. 
- Finally, this class also maintains the difficulty level that a block uses for mining. 

5. Driver Code (driver_code.py)
- This is main code for implementing complete blockchain, as per various users registered onto the network & the various transactions that happen between them.

#### Assumptions

For the sake of this project, I have limited my coding scope to following assumptions (which may or may not hold true in case of real world block-chain technologies): 

1. One user can have only one wallet. 
2. One wallet will hold only one private key and its corresponding public key, which will be generated or loaded during wallet creation. 
3. If the private and public key for a user wallet are already created and stored in the project folder by serialising them, then these keys will not be created again. The already stored keys will be loaded for use.
4. Please note that the keys should be stored inside the project folder (where they are stored by default, on serialisation). If they are stored anywhere else, they will not be fetched and program will consider keys to be missing. 
5. However, if the private and public keys for a user are already created once, but not stored by serialising them, then these keys will be generated again when the program is run again, as the keys previously generated cannot be fetched. 



Thanks!

Priyanka Reddy
