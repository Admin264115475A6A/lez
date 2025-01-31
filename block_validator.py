import os
import hashlib
import json
from datetime import datetime


class Block:
    def __init__(self, index, timestamp, data, previous_hash, difficulty=4):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0  # Start with a nonce of 0
        self.hash = self.calculate_hash()
        self.difficulty = difficulty  # Number of leading zeroes required

    def calculate_hash(self):
        """
        Calculate the SHA-256 hash of the block using its attributes, including the nonce.
        """
        block_string = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(block_string.encode('utf-8')).hexdigest()

    def mine_block(self):
        """
        Perform proof-of-work by adjusting the nonce until the hash satisfies the difficulty.
        """
        while not self.hash.startswith('0' * self.difficulty):
            self.nonce += 1
            self.hash = self.calculate_hash()

        print(f"Block {self.index} mined with nonce: {self.nonce} and hash: {self.hash}")


class Blockchain:
    def __init__(self, directory, difficulty=4):
        self.chain = []
        self.directory = directory
        self.difficulty = difficulty
        self.create_genesis_block()
        self.load_blocks_from_files()

    def create_genesis_block(self):
        """
        Create the first block (Genesis Block) in the blockchain.
        """
        genesis_block = Block(0, str(datetime.now()), "Genesis Block", "0", self.difficulty)
        genesis_block.mine_block()  # Mine the genesis block
        self.chain.append(genesis_block)

    def load_blocks_from_files(self):
        """
        List all block_X.txt files and load their content into the blockchain as new blocks.
        """
        block_files = [f for f in os.listdir(self.directory) if f.startswith("block_") and f.endswith(".txt")]
        block_files.sort()  # Ensure blocks are loaded in the correct order

        for block_file in block_files:
            file_path = os.path.join(self.directory, block_file)
            with open(file_path, 'r') as file:
                block_data = file.read()

            # Add a new block to the blockchain
            self.add_block(block_data)

    def add_block(self, data):
        """
        Add a new block to the blockchain by mining it.
        """
        previous_block = self.chain[-1]
        new_block = Block(len(self.chain), str(datetime.now()), data, previous_block.hash, self.difficulty)
        new_block.mine_block()  # Mine the new block
        self.chain.append(new_block)

    def is_chain_valid(self):
        """
        Verify the integrity of the blockchain.
        """
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            # Check if the current block's hash is valid
            if current_block.hash != current_block.calculate_hash():
                return False

            # Check if the current block's previous hash matches the previous block's hash
            if current_block.previous_hash != previous_block.hash:
                return False

        return True

    def save_to_json(self, json_file_path):
        """
        Export the blockchain to a JSON file.
        """
        blockchain_data = []
        for block in self.chain:
            blockchain_data.append({
                "index": block.index,
                "timestamp": block.timestamp,
                "data": block.data,
                "previous_hash": block.previous_hash,
                "nonce": block.nonce,
                "hash": block.hash
            })

        with open(json_file_path, 'w') as json_file:
            json.dump(blockchain_data, json_file, indent=4)

        print(f"Blockchain exported to {json_file_path}")

def print_all_blocks(self):
        """
        Print all blocks data to the terminal.
        """
        for block in self.chain:
            print(f"Block {block.index}:")
            print(f"  Timestamp: {block.timestamp}")
            print(f"  Data: {block.data}")
            print(f"  Previous Hash: {block.previous_hash}")
            print(f"  Nonce: {block.nonce}")
            print(f"  Hash: {block.hash}")
            print('-' * 40)  # Print a separator for better readability


# Example usage
if __name__ == "__main__":
    # Directory containing block_X.txt files
    directory = r"C:\Users\vlad\OneDrive\Desktop\os\mint_tea\medusacoin\lenz-main\coin\block"  # Update this path as needed

    # Create a blockchain and load blocks from files
    blockchain = Blockchain(directory, difficulty=4)

    # Check if the blockchain is valid
    if blockchain.is_chain_valid():
        print("Blockchain is valid.")
    else:
        print("Blockchain is not valid.")

    # Print all block data to the terminal
    blockchain.print_all_blocks()

    # Export the blockchain to a JSON file
    blockchain.save_to_json(r"C:\Users\vlad\OneDrive\Desktop\os\mint_tea\medusacoin\lenz-main\coin\blockchain.json")
    