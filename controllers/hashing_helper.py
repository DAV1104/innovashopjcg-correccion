import hashlib
import os

# Hashes and salts passwords using SHA-256
def hash_password(password):
    salt = os.urandom(16)
    salted_password = password.encode('utf-8') + salt
    sha256_hash = hashlib.sha256(salted_password).hexdigest()
    return salt.hex() + sha256_hash

# Verifies the password by reverse engineering the above
def verify_password(stored_password, provided_password):
    try:
        salt = bytes.fromhex(stored_password[:32])
        stored_hash = stored_password[32:]
        salted_password = provided_password.encode('utf-8') + salt
        sha256_hash = hashlib.sha256(salted_password).hexdigest()
        return stored_hash == sha256_hash
    except ValueError:
        return stored_password == provided_password