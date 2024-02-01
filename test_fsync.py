import os
import shutil
import hashlib
import time
import pytest
from subprocess import run, PIPE

@pytest.fixture
def temp_dir():
    temp_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), 'temp'))
    os.makedirs(temp_dir, exist_ok=True)
    yield temp_dir
    shutil.rmtree(temp_dir)

@pytest.fixture
def source_dir(temp_dir):
    source_dir = os.path.join(temp_dir, 'source')
    os.makedirs(source_dir, exist_ok=True)
    return source_dir

@pytest.fixture
def replica_dir(temp_dir):
    replica_dir = os.path.join(temp_dir, 'replica')
    return replica_dir

def calculate_md5(file_path):
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()

def test_basic_synchronization(source_dir, replica_dir):
    # Set up source folder
    with open(os.path.join(source_dir, 'test.txt'), 'w') as f:
        f.write('Hello, World!')

    # Run the script
    command = ['python3', 'fsync.py', source_dir, replica_dir, '1', 'log.txt']
    run(command, stdout=PIPE, stderr=PIPE)

    # Verify
    assert os.path.exists(os.path.join(replica_dir, 'test.txt'))

def test_periodic_synchronization(source_dir, replica_dir):
    # Set up source folder
    with open(os.path.join(source_dir, 'test.txt'), 'w') as f:
        f.write('Hello, World!')

    # Run the script
    command = ['python3', 'fsync.py', source_dir, replica_dir, '1', 'log.txt']
    process = run(command, stdout=PIPE, stderr=PIPE)

    # Modify source during synchronization
    time.sleep(2)
    with open(os.path.join(source_dir, 'test.txt'), 'a') as f:
        f.write(' Updated')

    process.communicate()

    # Verify
    assert 'Updated' in open(os.path.join(replica_dir, 'test.txt')).read()

def test_created_folder_synchronization(source_dir, replica_dir):
    # Set up source folder with a new subfolder
    new_folder = os.path.join(source_dir, 'new_folder')
    os.makedirs(new_folder, exist_ok=True)

    # Run the script
    command = ['python3', 'fsync.py', source_dir, replica_dir, '1', 'log.txt']
    run(command, stdout=PIPE, stderr=PIPE)

    # Verify the new folder exists in the replica
    assert os.path.exists(os.path.join(replica_dir, 'new_folder'))

def test_removed_folder_synchronization(source_dir, replica_dir):
    # Set up source folder with an existing subfolder
    existing_folder = os.path.join(source_dir, 'existing_folder')
    os.makedirs(existing_folder, exist_ok=True)

    # Run the script
    command = ['python3', 'fsync.py', source_dir, replica_dir, '1', 'log.txt']
    run(command, stdout=PIPE, stderr=PIPE)

    # Remove the subfolder from the source
    shutil.rmtree(existing_folder)

    # Run the script again
    run(command, stdout=PIPE, stderr=PIPE)

    # Verify the existing folder is removed from the replica
    assert not os.path.exists(os.path.join(replica_dir, 'existing_folder'))


