from Account.Database import Model_Database, Model_Cryptography


class ControllerDatabase:

    def __init__(self):

        self.MODEL_CRYPTOGRAPHY: Model_Cryptography = Model_Cryptography.ModelCryptography()
        self.MODEL_DATABASE: Model_Database = Model_Database.ModelDatabase()

    def get_hash(self, password: str) -> str:

        return self.MODEL_CRYPTOGRAPHY.get_hash(password)

    def verify_hash(self, password_hash: str, password: str) -> bool:

        return self.MODEL_CRYPTOGRAPHY.verify_hash(password_hash, password)

    def encrypt_secret(self, secret: str, password: str) -> str:

        return self.MODEL_CRYPTOGRAPHY.encrypt_secret(secret, password)

    def decrypt_secret(self, encrypted_secret: str, password: str):

        return self.MODEL_CRYPTOGRAPHY.decrypt_secret(encrypted_secret, password)