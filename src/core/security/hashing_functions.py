from argon2 import PasswordHasher

ph = PasswordHasher()

def hash_password(plain_password):
    return ph.hash(plain_password)

def verify_password(plain_password, hashed_password):
    return ph.verify(plain_password, hashed_password)