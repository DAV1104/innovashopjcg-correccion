import hashlib
import os

#hashea y saltea las contraseñas a partir de un numero no random, y un algoritmo de codificacion md5
def hash_password(password):
    salt = os.urandom(16)
    salted_password = password.encode('utf-8') + salt
    md5_hash = hashlib.md5(salted_password).hexdigest()
    return salt.hex() + md5_hash

#verifica la contraseña mediante ingenieria inversa de lo anterior
def verify_password(stored_password, provided_password):
    try:
        salt = bytes.fromhex(stored_password[:32])
        stored_hash = stored_password[32:]
        salted_password = provided_password.encode('utf-8') + salt
        md5_hash = hashlib.md5(salted_password).hexdigest()
        return stored_hash == md5_hash
    except ValueError:
        return stored_password == provided_password
