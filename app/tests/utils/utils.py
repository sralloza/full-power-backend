import random
import string


def random_lower_string() -> str:
    return "".join(random.choices(string.ascii_lowercase, k=32))


def random_constrained_int(lower_limit: int, upper_limit: int) -> int:
    return random.randint(lower_limit, upper_limit)


def random_int() -> int:
    return int("".join(random.choices(string.digits, k=10)))


def random_bytes() -> bytes:
    return random_lower_string().encode("utf8")
