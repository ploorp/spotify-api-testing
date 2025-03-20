import os
from dotenv import load_dotenv
import spotipy

load_dotenv()

client_id = os.getenv("CLIENT_ID")