import sys
import os
from cleneshade.ceapi import CleneshadeAPI

def main():
    # Check if any arguments were passed
    if len(sys.argv) < 2:
        print("no file opened.")
        return

    file_to_run = sys.argv[1]

    # Verify the file actually exists on the disk
    if not os.path.exists(file_to_run):
        print(f"Error: File '{file_to_run}' not found.")
        return

    # Initialize the API and execute
    api = CleneshadeAPI()
    api.translate_and_run(file_to_run)

if __name__ == "__main__":
    main()