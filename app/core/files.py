from hashlib import sha256


def get_file_id_from_name(name: str, lang: str) -> str:
    return sha256(f"{name}{lang}".encode("utf8")).hexdigest()
