import hashlib
import time
import socket

class Block:
    def __init__(self, timestamp, data, previous_hash, proof):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.proof = proof
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculate the hash of the block."""
        block_string = f"{self.timestamp}{self.data}{self.previous_hash}{self.proof}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        """Create the first block in the blockchain."""
        return Block(time.time(), "Genesis block", "0", "0")

    def add_block(self, new_block):
        """Add a new block to the blockchain."""
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()
        self.chain.append(new_block)

    def add_transaction(self, transaction):
        """Add a new transaction to the list of pending transactions."""
        self.pending_transactions.append(transaction)

    def get_latest_block(self):
        """Return the latest block in the blockchain."""
        return self.chain[-1]

    def is_chain_valid(self):
        """Check if the blockchain is valid."""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                return False
            if current_block.previous_hash != previous_block.hash:
                return False
        return True

def proof_of_work(block, difficulty):
    """Calculate the proof of work for a block."""
    proof = 0
    while not valid_proof(block, proof, difficulty):
        proof += 1
    return proof

def valid_proof(block, proof, difficulty):
    """Check if a proof of work is valid for a block."""
    block_string = f"{block.timestamp}{block.data}{block.previous_hash}{proof}"
    hash = hashlib.sha256(block_string.encode()).hexdigest()
    return hash[:difficulty] == "0" * difficulty

class Node:
    def __init__(self, host, port, blockchain):
        self.host = host
        self.port = port
        self.blockchain = blockchain
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((self.host, self.port))
        self.server_socket.listen()

    def listen_for_connections(self):
        """Listen for incoming connections from other nodes."""
        while True:
            connection, address = self.server_socket.accept()
            print(f"Received connection from {address}")
            connection.send("Welcome to the blockchain!".encode())
            connection.close()

# # Create the first node and start listening for connections
# node1 = Node("10.0.0.1", 8000, Blockchain())  # Replace "10.0.0.1" with the IP address of the first machine
# node1.listen_for_connections()

# # Create a second node and connect to the first node
# node2 = Node("10.0.0.2", 8001, Blockchain())  # Replace "10.0.0.2" with the IP address of the second machine
# client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# client_socket.connect(("10.0.0.1", 8000))  # Replace "10.0.0.1" with the IP address of the first machine
# response = client_socket.recv(1024).decode()
# print(response)  # Output: "Welcome to the blockchain!"
# client_socket.close()

# Create a new blockchain and start listening for connections
blockchain = Blockchain()
node1 = Node("localhost", 8000, blockchain)
node1.listen_for_connections()


# Create a new node and connect to the first node
node2 = Node("localhost", 8001, Blockchain())
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect(("localhost", 8000))
response = client_socket.recv(1024).decode()
print(response)  # Output: "Welcome to the blockchain!"
client_socket.close()
