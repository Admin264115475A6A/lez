import os

# Path to the shutdown signal file
shutdown_file = r"\coin\shutdown.txt"

# Create the shutdown signal
def trigger_shutdown():
    try:
        with open(shutdown_file, "w") as f:
            f.write("Shutdown requested.")
        print("Shutdown signal created.")
    except Exception as e:
        print(f"Error creating shutdown signal: {e}")

# Trigger the shutdown
if __name__ == "__main__":
    trigger_shutdown()
