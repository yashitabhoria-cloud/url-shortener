import os

from dotenv import load_dotenv


load_dotenv()


API_KEY = os.getenv("API_KEY")

RATE_LIMIT_REQUESTS = int(os.getenv("RATE_LIMIT_REQUESTS", "100"))
RATE_LIMIT_WINDOW_SECONDS = int(os.getenv("RATE_LIMIT_WINDOW_SECONDS", "60"))

if API_KEY is None:
    raise RuntimeError("API_KEY environment variable is not set")