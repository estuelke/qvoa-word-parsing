import sys
from app.process_data import process_data

if __name__ == "__main__":
    filenames = sys.argv[1:]
    process_data(filenames)
