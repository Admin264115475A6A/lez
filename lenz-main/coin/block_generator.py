import random
import hashlib
import time
import os
import threading
import json

# Function to write to a block file
def write_to_block_file(decoded_text, block_number):
    block_file = f"C:/Users/vlad/OneDrive/Desktop/os/mint_tea/block/block_{block_number}.txt"
    with open(block_file, "a") as f:
        f.writelines(decoded_text)
    print(f"Done writing to {block_file}")

# Function to count block_X.txt files in the directory
def count_block_files(directory):
    # Get all files in the directory that match the pattern block_X.txt
    block_files = [f for f in os.listdir(directory) if f.startswith("block_") and f.endswith(".txt")]
    return len(block_files)

# Example usage in your main loop
directory = "C:/Users/vlad/OneDrive/Desktop/os/mint_tea/block"  # Update this to your directory path

# Print the number of block_X.txt files in the directory
num_block_files = count_block_files(directory)
print(f"There are {num_block_files} block_X.txt files in the directory.")

# Set the duration for the loop (in seconds)
duration = 10 * 60  # 10 minutes
start_time = time.time()

# Random number generator loop
while True:
    
    # Seed generator loop creates six numbers
    x = []  # list
    for ii in range(6):
        A = random.randint(11, 99)
        x.append(A)

    a = x[0]
    b = x[1]
    c = x[2]
    d = x[3]
    e = x[4]
    f = x[5]

    # My table for seed generation
    ranZero = (a, b, c, d, e, f)
    ranOne = a + b + c + d + e + f
    ranTwo = a + 1 + b + 2 + c + 3 + d + 4 + e + 5 + f + 6
    ranThree = a + 1 + 3 + b + 2 + 5 + c + 3 + 7 + d + 4 + 11 + e + 5 + 13 + f + 6 + 17

    # Create seeds
    seedOne = ranOne * 16 * 2 ** 256
    seedTwo = ranTwo * 32 * 2 ** 256
    seedThr = ranThree * 64 * 2 ** 256

    # Generate seed values
    seed_gen_16 = str(seedOne * 16 ** 256)
    seed_gen_32 = str(seedTwo * 32 ** 256)
    seed_gen_64 = str(seedThr * 64 ** 256)

    # SHA512 hash for the seed_gen
    origin_seed = hashlib.sha512()
    origin_seed.update(str(seed_gen_16).encode('utf-8'))
    origin_seed.hexdigest()
    hsh = origin_seed.hexdigest()

    # Split and process seed_gen_16 into ASCII
    seed_gen_16 = str(seedOne * 16 ** 256)
    segment_width = 2  # ASCII values are 3 digits at most (0–127)
    segments = [seed_gen_16[i:i+segment_width] for i in range(0, len(seed_gen_16), segment_width)]

    # Convert each segment to ASCII (if valid)
    ascii_results = []
    for segment in segments:
        try:
            num = int(segment)  # Convert the segment to an integer
            if 0 <= num <= 127:  # Check if the number is in the ASCII range
                ascii_results.append(chr(num))  # Convert to ASCII character
            else:
                ascii_results.append('?')  # Placeholder for invalid values
        except ValueError:
            ascii_results.append('?')  # Handle non-convertible segments

    # Join the ASCII characters to form the final string
    ascii_string = ''.join(ascii_results)

    # Decode ASCII values to text
    decoded_text = ''.join([char for char in ascii_string])
    ascii_codes = [ord(char) for char in ascii_string]
    print("ASCII Codes:", ascii_codes)
    print("Decoded Text:", decoded_text)

    # Determine the file name (block_0.txt, block_1.txt, etc.)
    block_number = 0
    while os.path.exists(f"C:/Users/vlad/OneDrive/Desktop/os/mint_tea/block/block_{block_number}.txt"):
        block_number += 1  # Increment block number if the file exists

    # Create a thread to handle writing to the block file
    threading.Thread(target=write_to_block_file, args=(decoded_text, block_number)).start()

    # Inside the main loop, you can print the number of files after each write operation
    num_block_files = count_block_files(directory)
    print(f"There are {num_block_files} block_X.txt files in the directory.")

    # Write to seedgenTX.txt file
    with open("C:/Users/vlad/OneDrive/Desktop/os/mint_tea/medusacoin/lenz-main/crypto/blockchain/seedgenTX.txt", 'w') as f:
        f.writelines("seedgen file number generator")
        f.writelines("\n")
        f.writelines("\n")
        f.writelines("seed_gen_16: ")
        f.writelines(seed_gen_16)
        f.writelines("\n")
        f.writelines("seed_gen_32: ")
        f.writelines(seed_gen_32)
        f.writelines("\n")
        f.writelines("seed_gen_64: ")
        f.writelines(seed_gen_64)
        f.writelines("\n")
        f.writelines("origin_seed : ")
        f.writelines(origin_seed.hexdigest())
        f.writelines("\n")
        f.writelines("\n")

    print(f"done... please check the seedgenTX.txt")

    # Check if 10 minutes have passed
    elapsed_time = time.time() - start_time
    if elapsed_time >= duration:
        print("10 minutes have passed.")
        break

    # Wait for a short time before repeating the loop (optional)
    time.sleep(1)

    # Function to count block_X.txt files and generate a list of their names
    def list_block_files(directory):
        # Get all files in the directory that match the pattern block_X.txt
        block_files = [f for f in os.listdir(directory) if f.startswith("block_") and f.endswith(".txt")]
        return block_files

    # Function to write the block file names to a JSON file
    def write_block_files_to_json(directory, json_file_path):
        # Get the list of block files
        block_files = list_block_files(directory)

        # Prepare the data to be written in JSON format
        data = {
            "block_files": block_files
        }

        # Write the data to a JSON file
        with open(json_file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

        print(f"Block file list written to {json_file_path}")

    # Example usage in your main loop
    directory = "C:/Users/vlad/OneDrive/Desktop/os/mint_tea/block"  # Update this to your directory path
    json_file_path = "C:/Users/vlad/OneDrive/Desktop/os/mint_tea/block_files.json"  # Path to save the JSON file

    # Create and write the JSON file
    write_block_files_to_json(directory, json_file_path)

