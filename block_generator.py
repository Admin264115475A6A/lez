import random
import hashlib
import time
import os
import threading
import json
import logging
import configparser
from concurrent.futures import ThreadPoolExecutor

# Set up comprehensive logging
log_file_path = r"E:\coin\execution.log"  # Path to the execution log file

# Create a custom logger
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)  # Capture all levels (DEBUG, INFO, WARNING, ERROR, CRITICAL)

# Create a file handler that writes to execution.log
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel(logging.DEBUG)  # Capture all levels for file logs

# Create a console handler to display logs on the console (optional)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)  # Display INFO and above in the console

# Create a formatter and attach it to the handlers
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


# Read configuration from config.ini
config = configparser.ConfigParser()
config.read(r"E:\coin\config.ini")

# Load file paths from the configuration file
directory = config.get('paths', 'directory')
shutdown_file = config.get('paths', 'shutdown_file')
seedgen_file = config.get('paths', 'seedgen_file')
json_file_path = config.get('paths', 'block_files_json')
log_file = config.get('paths', 'log_file', fallback=r"E:\coin\error.log")

# Configure logging for error tracking
logging.basicConfig(
    filename=log_file,
    level=logging.ERROR,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Thread locks for synchronization
lock = threading.Lock()
json_lock = threading.Lock()

# ThreadPoolExecutor for managing threads
thread_pool = ThreadPoolExecutor(max_workers=5)

# Helper function for safe file operations
def safe_file_operation(action, *args, **kwargs):
    """
    Perform safe file operations with error handling and logging.
    """
    try:
        return action(*args, **kwargs)
    except Exception as e:
        logging.error(f"Error during file operation: {e}")
        return None

# Function to list files with a specific prefix and suffix
def list_files_with_prefix(directory, prefix, suffix=""):
    """
    List all files in the specified directory that match the given prefix and suffix.
    """
    return safe_file_operation(
        lambda: [
            f for f in os.listdir(directory)
            if f.startswith(prefix) and f.endswith(suffix)
        ]
    ) or []

# Function to determine the next block number
def get_next_block_number(directory, prefix="block_", suffix=".txt"):
    """
    Find the next available block number based on existing block files.
    """
    files = list_files_with_prefix(directory, prefix, suffix)
    if files:
        numbers = [
            int(f[len(prefix):-len(suffix)]) for f in files if f[len(prefix):-len(suffix)].isdigit()
        ]
        return max(numbers, default=-1) + 1
    return 0

# Function to write data to a block file
def write_to_block_file(decoded_text, block_number):
    """
    Append data to the corresponding block file.
    """
    block_file = os.path.join(directory, f"block_{block_number}.txt")
    with open(block_file, "a") as f:
        f.writelines(decoded_text)
    logging.info(f"Done writing to {block_file}")

# Function to update block file list in JSON
def write_block_files_to_json():
    """
    Updates the JSON file with the current list of block files.
    """
    try:
        with json_lock:
            block_files = list_files_with_prefix(directory, "block_", ".txt")
            data = {"block_files": block_files}
            safe_file_operation(lambda: json.dump(data, open(json_file_path, "w"), indent=4))
            logging.info(f"Block file list updated in {json_file_path}")
    except Exception as e:
        logging.error(f"Error updating block file list in JSON: {e}")

# Function to check for a shutdown signal
def check_for_shutdown_signal(signal_file):
    """
    Checks if a shutdown file exists, signaling termination.
    """
    return os.path.exists(signal_file)

# Convert seed value to ASCII representation
def convert_to_ascii(seed_str):
    """
    Convert numeric seed string to ASCII characters where possible.
    """
    return ''.join(
        chr(int(seed_str[i:i+2])) if seed_str[i:i+2].isdigit() and 0 <= int(seed_str[i:i+2]) <= 127 else '?' 
        for i in range(0, len(seed_str), 2)
    )

# Thread lock for writing to the seedgen_file
seedgen_lock = threading.Lock()

# Function to generate seed values and write blocks
def generate_and_write_block():
    """
    Generates random seeds, computes hashes, converts to ASCII, and writes to a block file.
    """
    # Generate random numbers
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

    # Compute SHA-512 hashes
    hashed_seeds = [hashlib.sha512(str(seed).encode('utf-8')).hexdigest() for seed in seeds]

    # Log seed generation
    logging.info(f"Generated seeds: {seeds}")

    # Write seed data to file (with lock to prevent race conditions)
    with seedgen_lock:
        seed_data = [
            f"seed_gen_{2**i}: {seeds[i]}\n"
            f"hash_{2**i}: {hashed_seeds[i]}\n"
            for i in range(3)
        ]
        safe_file_operation(lambda: open(seedgen_file, "w").writelines(["seedgen file number generator\n\n"] + seed_data))
        logging.info(f"Seed file written to {seedgen_file}")

    # Convert first seed to ASCII
    seed_16_str = str(seeds[0])
    ascii_string = convert_to_ascii(seed_16_str)
    logging.info(f"Converted first seed to ASCII: {ascii_string}")

    # Get next block number and write block data
    with lock:
        block_number = get_next_block_number(directory)
        logging.info(f"Next block number determined: {block_number}")
        thread_pool.submit(write_to_block_file, ascii_string, block_number)
        thread_pool.submit(write_block_files_to_json)

# Main loop with shutdown handling
try:
    logging.info("Block generator started.")
    duration = 10 * 60  # 10 minutes
    start_time = time.time()

    while True:
        # Check for shutdown signal
        if check_for_shutdown_signal(shutdown_file):
            logging.info("Shutdown signal detected. Exiting safely...")
            break

        # Generate and write a new block
        generate_and_write_block()

        # Check if the duration has elapsed
        if time.time() - start_time >= duration:
            logging.info("10 minutes have passed.")
            break   

        time.sleep(1)  # Short pause to prevent excessive CPU usage
except KeyboardInterrupt:
    logging.info("Process interrupted by user. Exiting gracefully...")
finally:
    # Shutdown the thread pool and wait for tasks to finish
    thread_pool.shutdown(wait=True)
    logging.info("ThreadPoolExecutor has been shut down.")
