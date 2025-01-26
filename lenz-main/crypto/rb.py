import struct
from collections import Counter
import matplotlib.pyplot as plt
from PIL import Image
import os
import wave
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

# Define file path
file_path = "random_file_custom.bin"

# Reading all bytes of the binary file
with open(file_path, "rb") as f:
    all_binary_data = f.read()

# Decode all bytes as hexadecimal
all_hex_data = all_binary_data.hex()

# Decode all bytes as text (with error replacement for unprintable characters)
all_text_data = all_binary_data.decode(errors="replace")

# Print lengths and first 1024 characters
print(f"Length of Hex Data: {len(all_hex_data)}")
print(f"Length of Text Data: {len(all_text_data)}")
print("First 1024 Hex Characters:", all_hex_data[:1024000])
print("First 1024 Text Characters:", all_text_data[:1024000])

# Count the frequency of each byte in the file
byte_counts = Counter(all_binary_data)

# Calculate basic statistics
total_bytes = len(all_binary_data)
unique_bytes = len(byte_counts)
most_common_bytes = byte_counts.most_common(100)  # Top 100 most frequent bytes

# Output the analysis
print("Total Bytes:", total_bytes)
print("Unique Bytes:", unique_bytes)
print("Most Common Bytes:", most_common_bytes)

# Example display of first few bytes
print("Hexadecimal (First 64 bytes):", all_binary_data[:64].hex())
print("Text Representation (First 64 bytes):", all_binary_data[:64].decode(errors="replace"))

# Attempt to decode the binary data as a sequence of integers (assuming 32-bit integers)
integer_data = []
try:
    integer_data = list(struct.unpack(f"{len(all_binary_data) // 4}i", all_binary_data))
except struct.error as e:
    integer_data = str(e)  # Capture the error if the data isn't properly aligned for integers

# Show the first 256 integers if available
if isinstance(integer_data, list):
    print("First 256 Integers:", integer_data[:1024])
else:
    print("Integer decoding error:", integer_data)

# Plot the decoded integer data
if isinstance(integer_data, list) and len(integer_data) > 0:
    plt.figure(figsize=(10, 64))
    plt.plot(integer_data[:64], marker='o', linestyle='-', color='b')  # Plot the first 256 integers
    plt.title("Plot of Decoded Integer Data")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.grid(True)
    plt.show()
else:
    print("Plot skipped: No valid integer data.")


    
import matplotlib.pyplot as plt

# Data for the bar graph
categories = ["Most Common Bytes", "Total Bytes", "Unique Bytes", "Integer Data"]
values = [
    len(byte_counts.most_common(100)),  # Most common bytes (top 100)
    len(all_binary_data),              # Total bytes
    len(byte_counts),                  # Unique bytes
    len(integer_data) if isinstance(integer_data, list) else 0  # Integer data count
]

# Plotting the bar graph
plt.figure(figsize=(10, 6))
plt.bar(categories, values, color=['skyblue', 'orange', 'green', 'purple'], edgecolor='black')
plt.title("Binary File Analysis Summary", fontsize=14)
plt.xlabel("Categories", fontsize=12)
plt.ylabel("Count", fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()

# converts random_file.bin into a image

# Load the binary data
with open('random_file_custom.bin', 'rb') as f:
    data = f.read()

# Calculate dimensions for a square image
image_size = int(len(data) ** .5)  # Assuming a square image

# Truncate the data if it's not a perfect square
data = data[:image_size * image_size]

# Create a grayscale image
img = Image.frombytes('L', (image_size, image_size), data)

# Save the image
img.save('random_image_rb.png')

print("Image generated and saved as random_image_rb.png.")

# converts random_file.bin to sound file with the wave extention

# Open the binary file and read the data
with open('random_file_custom.bin', 'rb') as f:
    data = f.read()

# Parameters for the .wav file
num_channels = 1        # Mono
sample_width = 2        # 2 bytes (16 bits per sample)
frame_rate = 44100      # Standard frame rate for audio
num_frames = len(data) // sample_width  # Number of frames we can create

# Ensure the data length is a multiple of the sample width (16 bits = 2 bytes)
data = data[:num_frames * sample_width]

# Convert the binary data to 16-bit integers
samples = struct.unpack('<' + 'h' * (len(data) // sample_width), data)

# Write to a .wav file
with wave.open('random_sound_custom.wav', 'w') as wav_file:
    wav_file.setnchannels(num_channels)
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(frame_rate)
    wav_file.writeframes(struct.pack('<' + 'h' * len(samples), *samples))

print("Random sound file generated as random_sound.wav.")

