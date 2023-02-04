import os
from dotenv import load_dotenv


load_dotenv()

PLAYER_FILE_PATH = os.environ["PLAYER_FILE_PATH"]
VERBOSE = os.environ["VERBOSE"] == "True"
PORT = os.environ["PORT"]
