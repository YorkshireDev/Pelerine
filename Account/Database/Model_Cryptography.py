from werkzeug.security import generate_password_hash, check_password_hash
from cryptocode import encrypt, decrypt


class ModelCryptography:

    def __init__(self):

        self.HASH_METHOD: str = "pbkdf2:sha512:1048576"
        self.SALT_LENGTH: int = 256

    def get_hash(self, password: str) -> str:

        return generate_password_hash(password, self.HASH_METHOD, self.SALT_LENGTH)

    @staticmethod
    def verify_hash(password_hash: str, password: str) -> bool:

        return check_password_hash(password_hash, password)

    @staticmethod
    def encrypt_secret(secret: str, password: str) -> str:

        return encrypt(secret, password)

    @staticmethod
    def decrypt_secret(encrypted_secret: str, password: str) -> bool | str:

        return decrypt(encrypted_secret, password)
