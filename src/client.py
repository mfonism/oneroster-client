import os

from dotenv import load_dotenv

load_dotenv()


def ping() -> str:
    return "It works!"


def pong() -> str:
    return os.getenv("PONG")
