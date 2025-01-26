from PIL import Image
import os
import wave
import struct


#generate a random_file.bin 

# Set the file size in bytes (1 megabit = 125,000 bytes)
file_size = 125000

# Generate random bytes
random_data = os.urandom(file_size)

# Write the random bytes to a file
with open('random_file.bin', 'wb') as f:
    f.write(random_data)

print("1 Megabit random file generated successfully.")

# converts random_file.bin to sound file with the wave extention

# Open the binary file and read the data
with open('random_file.bin', 'rb') as f:
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
with wave.open('random_sound.wav', 'w') as wav_file:
    wav_file.setnchannels(num_channels)
    wav_file.setsampwidth(sample_width)
    wav_file.setframerate(frame_rate)
    wav_file.writeframes(struct.pack('<' + 'h' * len(samples), *samples))

print("Random sound file generated as random_sound.wav.")


# converts random_file.bin into a image

# Load the binary data
with open('random_file.bin', 'rb') as f:
    data = f.read()

# Calculate dimensions for a square image
image_size = int(len(data) ** .5)  # Assuming a square image

# Truncate the data if it's not a perfect square
data = data[:image_size * image_size]

# Create a grayscale image
img = Image.frombytes('L', (image_size, image_size), data)

# Save the image
img.save('random_image.png')

print("Image generated and saved as random_image.png.")


# generating an image to png to bin

# Open the image and prepare to write pixel data to a binary file
with Image.open("random_image.png") as im:
    px = im.load()

# Open the binary file for writing
with open("image.bin", "wb") as out_file:
    for y in range(256):
        for x in range(256):
            # Get the pixel at (x, y) (assuming it's an RGB or RGBA image)
            pixel = px[x, y]
            
            # If it's RGB, pixel is a tuple of 3 values (R, G, B)
            # If it's RGBA, pixel is a tuple of 4 values (R, G, B, A)
            if isinstance(pixel, tuple):
                # Write the pixel values to the binary file as bytes
                out_file.write(struct.pack('B' * len(pixel), *pixel))
            else:
                # For grayscale images, pixel might be a single value
                out_file.write(struct.pack('B', pixel))



#generate an image from the random_sound.wav


import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from scipy import signal

# Load the wav file
wav_file = 'random_sound.wav'

# Read the wav file (waveform) using scipy
sample_rate, samples = wavfile.read(wav_file)

# Create a figure for the images
plt.figure(figsize=(12, 6))

# Plot the waveform
plt.subplot(1, 2, 1)
plt.plot(np.linspace(0, len(samples) / sample_rate, num=len(samples)), samples)
plt.title('Waveform')
plt.xlabel('Time [s]')
plt.ylabel('Amplitude')

# Generate and plot the spectrogram
plt.subplot(1, 2, 2)
frequencies, times, spectrogram = signal.spectrogram(samples, sample_rate)
plt.pcolormesh(times, frequencies, 10 * np.log10(spectrogram), shading='gouraud')
plt.title('Spectrogram')
plt.ylabel('Frequency [Hz]')
plt.xlabel('Time [s]')

# Save the image as a PNG file
plt.savefig('audio_visualization.png')
plt.show()

print("Image generated and saved as audio_visualization.png.")


