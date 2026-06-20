import random
import string
import re


def generate_short_code(length: int = 6) -> str:
    characters = string.ascii_letters + string.digits
    return "".join(random.choice(characters) for _ in range(length))


def is_valid_custom_code(custom_code: str) -> bool:
    pattern = r"^[a-zA-Z0-9_-]{3,20}$"
    return re.match(pattern, custom_code) is not None