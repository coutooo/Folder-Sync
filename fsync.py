import os
import argparse
import time
from datetime import datetime
import hashlib
import shutil

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def copy_file(source_path, replica_path, log_file):
    try:
        with open(source_path, 'rb') as source_file:
            with open(replica_path, 'wb') as replica_file:
                log_message = f"{datetime.now()} - Copying {source_path} to {replica_path}\n"
                log_to_file(log_file, log_message)
                print(log_message)
                replica_file.write(source_file.read())


    except Exception as e:
        error_message = f"{datetime.now()} - Error copying {source_path} to {replica_path}: {str(e)}\n"
        log_to_file(log_file, error_message)
        print(error_message)

def sync_folders(source, replica, log_file):
    if not os.path.exists(replica):
        log_message = f"{datetime.now()} - Created folder {replica}\n"
        log_to_file(log_file, log_message)
        print(log_message)
        os.makedirs(replica)

    for root, dirs, files in os.walk(source):
        for file in files:
            source_path = os.path.join(root, file)
            replica_path = os.path.join(replica, os.path.relpath(source_path, source))

            if not os.path.exists(replica_path) or calculate_md5(source_path) != calculate_md5(replica_path):
                copy_file(source_path, replica_path, log_file)
    
        for dir in dirs:
            source_path = os.path.join(root, dir)
            replica_path = os.path.join(replica, os.path.relpath(source_path, source))

            if not os.path.exists(replica_path):
                os.makedirs(replica_path)
                log_message = f"{datetime.now()} - Created folder {replica_path}\n"
                log_to_file(log_file, log_message)
                print(log_message)
    
    # Remove files/directories in replica that are not in source
    for root, dirs, files in os.walk(replica):
        for file in files:
            replica_path = os.path.join(root, file)
            source_path = os.path.join(source, os.path.relpath(replica_path, replica))

            if not os.path.exists(source_path):
                os.remove(replica_path)
                log_message = f"{datetime.now()} - Removed {replica_path}\n"
                log_to_file(log_file, log_message)
                print(log_message)
    
        for dir in dirs:
            replica_path = os.path.join(root, dir)
            source_path = os.path.join(source, os.path.relpath(replica_path, replica))

            if not os.path.exists(source_path):
                shutil.rmtree(replica_path)
                log_message = f"{datetime.now()} - Removed folder {replica_path}\n"
                log_to_file(log_file, log_message)
                print(log_message)

def log_to_file(log_file, message):
    with open(log_file, "a") as file:
        file.write(message)

def main():
    parser = argparse.ArgumentParser(description='Folder synchronization')
    parser.add_argument("source", help="Path to the source folder")
    parser.add_argument("replica", help="Path to the replica folder")
    parser.add_argument("interval", type=int, help="Synchronization interval in seconds")
    parser.add_argument("log_file", help="Path to the log file")

    args = parser.parse_args()

    while True:
        sync_folders(args.source, args.replica, args.log_file)
        time.sleep(args.interval)

if __name__ == "__main__":
    import sys
    if "pytest" not in sys.argv[0]:  # Exclude this block when running tests with pytest
        main()
