import os
from dotenv import load_dotenv
from sys import argv

load_dotenv()

if "PLAYER_FILE_PATH" in os.environ:
    PLAYER_FILE_PATH = os.environ["PLAYER_FILE_PATH"]
else: 
    PLAYER_FILE_PATH = argv[1]
    
VERBOSE = os.environ["VERBOSE"] == "True"
PORT = os.environ["PORT"]
