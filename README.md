# Folder Synchronization

This project provides a simple Python script for one-way synchronization of folders. The script ensures that the contents of the replica folder exactly match the content of the source folder. File creation, copying, removal operations are logged to both the console output and a log file.

## Features

- One-way synchronization from source to replica.
- Periodic synchronization at specified intervals.
- Logging of file operations to console and log file.

## Getting Started

### Prerequisites

- Python (version 3.x recommended)

### Installation

1. Clone the repository:

   ```bash
   git clone [https://github.com/your-username/folder-synchronization.git](https://github.com/coutooo/Folder-Sync.git)
   
2. Change into the project directory:
   
   ```bash
   cd Folder-Sync
4. Run the script with appropriate command line arguments:

   ```bash
   python3 fsync.py source_folder replica_folder synchronization_interval log_file_path

## Testing

The project includes test cases to ensure the correctness of synchronization logic. You can run the tests using pytest:
  ```bash
  python3 -m pytest -v test_fsync.py
