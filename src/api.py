import os

from dotenv import load_dotenv

load_dotenv()


class Client:
    def __init__(self):
        self.token_url = os.getenv("TOKEN_URL")
        self.base_url = os.getenv("BASE_URL")
