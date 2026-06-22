import os

from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("API_KEY")


if API_KEY is None:
    raise RuntimeError("API_KEY environment variable is not set")