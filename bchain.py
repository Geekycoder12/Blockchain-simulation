import hashlib
import time

class Block:
    def __init__(self, timestamp, data, previous_hash):
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        """Calculate the hash of the block."""
        block_string = f"{self.timestamp}{self.data}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.pending_transactions = []

    def create_genesis_block(self):
        """Create the first block in the blockchain."""
        return Block(time.time(), "Genesis block", "0")

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

# Create a new blockchain
blockchain = Blockchain()

# Add some transactions to the pending transactions list
blockchain.add_transaction("Alice sends 1 BTC to Bob")
blockchain.add_transaction("Bob sends 0.5 BTC to Alice")

# Create a new block and add it to the blockchain
new_block = Block(time.time(), blockchain.pending_transactions, blockchain.get_latest_block().hash)
blockchain.add_block(new_block)

# Reset the pending transactions list
blockchain.pending_transactions = []

# Check if the blockchain is valid
print(blockchain.is_chain_valid())  # Output: True
