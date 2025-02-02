import os
import subprocess
import time

# Paths to the scripts and shutdown file
shutdown_file = r"E:\coin\shutdown.txt"
block_generator_script = r"E:\coin\block_generator.py"

# Function to clean up shutdown signal before starting
def clean_shutdown_signal():
    if os.path.exists(shutdown_file):
        os.remove(shutdown_file)
        print("Old shutdown signal file removed.")

# Function to start the block generator script
def start_block_generator():
    try:
        print("Starting block generator...")
        # Use subprocess to launch the script
        subprocess.Popen(["python", block_generator_script], shell=True)
        print("Block generator started successfully.")
    except Exception as e:
        print(f"Error starting block generator: {e}")

# Main script logic
if __name__ == "__main__":
    print("Initializing system startup...")

    # Clean up any previous shutdown signal
    clean_shutdown_signal()

    # Start the block generator
    start_block_generator()

    # Notify user
    print("System is now running.")
    print("To stop the system, create the shutdown signal.")
