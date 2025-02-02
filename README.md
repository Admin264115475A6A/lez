# Block Generator
Project Name: Block Generator
Version: 1.0
Author: vladimir roush
## Overview
The **Block Generator** is a Python-based tool designed to generate cryptographic seeds, compute their hashes, and write them to a series of block files. The tool can run for a set duration or until a shutdown signal is received. It also manages these files in a directory and maintains an updated JSON file listing all the block files created. Additionally, the project includes a logging system to track the process, errors, and other events.

## Features
- Generate random seeds and compute SHA-512 hashes.
- Convert seed values into ASCII representation.
- Write the generated data to block files.
- Maintain a JSON file listing all block files created.
- Comprehensive logging of key events.
- Graceful handling of shutdown signals.

## Requirements
Make sure you have the following dependencies installed before running the program:

1. `random`
2. `hashlib`
3. `time`
4. `os`
5. `threading`
6. `json`
7. `logging`
8. `configparser`
9. `concurrent.futures` (for ThreadPoolExecutor)

These libraries are part of Python’s standard library and do not require separate installation.

## Dependencies

The following dependencies must be installed for the project to work:

```txt
# No external dependencies required. All dependencies are part of the Python standard library.
