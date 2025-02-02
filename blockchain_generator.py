import random
import hashlib
import time
import os
import threading
import json
import logging
import configparser
from datetime import datetime
from blockchain import Blockchain  # Import the Blockchain class from blockchain.py

# Read paths from config.ini
config = configparser.ConfigParser()
config.read(r"E:\coin\config.ini")

# Load paths from the configuration file
directory = config.get('paths', 'directory')
seedgen_file = config.get('paths', 'seedgen_file')
json_file_path = config.get('paths', 'block_files_json')
log_file = config.get('paths', 'log_file', fallback=r"E:\coin\error.log")

# Configure the logger
logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Thread-safe lock for shared resources
lock = threading.Lock()

# Helper Functions
def safe_file_operation(action, *args, **kwargs):
    """
    Wrapper to perform safe file operations with logging on errors.
    """
    try:
        return action(*args, **kwargs)
    except Exception as e:
        logging.error(f"Error during file operation: {e}")
        return None

def list_files_with_prefix(directory, prefix, suffix=""):
    """
    List files in a directory with a specific prefix and suffix.
    """
    return safe_file_operation(
        lambda: [
            f for f in os.listdir(directory)
            if f.startswith(prefix) and f.endswith(suffix)
        ]
    ) or []

def get_next_block_number(directory, prefix="block_", suffix=".txt"):
    """
    Find the next available block number for block files.
    """
    files = list_files_with_prefix(directory, prefix, suffix)
    if files:
        numbers = [
            int(f[len(prefix):-len(suffix)]) for f in files if f[len(prefix):-len(suffix)].isdigit()
        ]
        return max(numbers, default=-1) + 1
    return 0

# Function to write to a block file
def write_to_block_file(decoded_text, block_number):
    block_file = os.path.join(directory, f"block_{block_number}.txt")
    with open(block_file, "a") as f:
        f.writelines(decoded_text)
    print(f"Done writing to {block_file}")

# Function to write block file names to a JSON file
def write_block_files_to_json():
    block_files = list_files_with_prefix(directory, "block_", ".txt")
    data = {"block_files": block_files}
    safe_file_operation(
        lambda: json.dump(data, open(json_file_path, "w"), indent=4)
    )
    print(f"Block file list written to {json_file_path}")

# Duration for the loop (optional, can run indefinitely)
duration = 10 * 60  # 10 minutes
start_time = time.time()

# Initialize blockchain
blockchain = Blockchain(difficulty=3)  # Initialize the blockchain

# Main loop for generating blocks and interacting with the blockchain
while True:
    # Generate and write block to file
    x = [random.randint(11, 99) for _ in range(6)]
    ranOne = sum(x)
    ranTwo = ranOne + sum(range(1, 7))
    ranThr = sum(x[i] + sum(range(1, i + 2)) for i in range(6))

    # Generate seeds
    seeds = [
        ranOne * 16 * 2 ** 256,
        ranTwo * 32 * 2 ** 256,
        ranThr * 64 * 2 ** 256
    ]

    # Hash seeds
    def hash_seed(seed):
        return hashlib.sha512(str(seed).encode('utf-8')).hexdigest()

    hashed_seeds = [hash_seed(seed) for seed in seeds]

    # Write to seedgen file
    seed_data = [
        f"seed_gen_{2**i}: {seeds[i]}\n"
        f"hash_{2**i}: {hashed_seeds[i]}\n"
        for i in range(3)
    ]
    safe_file_operation(
        lambda: open(seedgen_file, "w").writelines(["seedgen file number generator\n\n"] + seed_data)
    )
    print(f"Seed file written to {seedgen_file}")

    # ASCII conversion
    seed_16_str = str(seeds[0])
    ascii_string = ''.join(
        chr(int(seed_16_str[i:i+2])) if seed_16_str[i:i+2].isdigit() and 0 <= int(seed_16_str[i:i+2]) <= 127 else '?'
        for i in range(0, len(seed_16_str), 2)
    )
    print(seed_16_str,"ascii", ascii_string, "ascii_string")
    # Write to block file
    with lock:
        block_number = get_next_block_number(directory)
        threading.Thread(target=write_to_block_file, args=(ascii_string, block_number)).start()

    # Prompt user to add a block to the blockchain only once during the loop
    if time.time() - start_time >= 5:  # Prompt after 5 seconds, or adjust as needed
        blockchain.add_block(input("Enter data for the new block: "))
        start_time = time.time()  # Reset timer after input

    # Check if 10 minutes have passed
    if time.time() - start_time >= duration:
        print("10 minutes have passed.")
        break
    time.sleep(1)
