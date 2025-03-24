import hashlib
import secrets
import base64


def hash_password(password: str, salt: bytes = None) -> tuple[str, str]:

    if salt is None:
        salt = secrets.token_bytes(16)

    salted_password = salt + password.encode('utf-8')
    hashed_password = hashlib.sha256(salted_password).digest()
    return base64.b64encode(hashed_password).decode('utf-8'), base64.b64encode(salt).decode('utf-8')


def verify_password(plain_password: str, hashed_password: str, salt: str) -> bool:

    salt_bytes = base64.b64decode(salt)
    salted_password = salt_bytes + plain_password.encode('utf-8')
    calculated_hash = hashlib.sha256(salted_password).digest()
    return base64.b64encode(calculated_hash).decode('utf-8') == hashed_password


# Example usage:
if __name__ == "__main__":
    password = "123456789"
    hashed, salt = hash_password(password)

    print(f"password: {password}")
    print(f"Hashed password: {hashed}")
    print(f"Salt: {salt}")

    is_valid = verify_password(password, hashed, salt)
    print(f"Password verification: {is_valid}")

    is_invalid = verify_password("wrongpassword", hashed, salt)
    print(f"Incorrect password verification: {is_invalid}")
