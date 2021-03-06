from Account.Database import Model_Database, Model_Cryptography


class ControllerDatabase:

    def __init__(self):

        self.MODEL_CRYPTOGRAPHY: Model_Cryptography = Model_Cryptography.ModelCryptography()
        self.MODEL_DATABASE: Model_Database = Model_Database.ModelDatabase(self)

    def get_hash(self, password: str) -> str:

        return self.MODEL_CRYPTOGRAPHY.get_hash(password)

    def verify_hash(self, password_hash: str, password: str) -> bool:

        return self.MODEL_CRYPTOGRAPHY.verify_hash(password_hash, password)

    def encrypt_secret(self, secret: str, password: str) -> str:

        return self.MODEL_CRYPTOGRAPHY.encrypt_secret(secret, password)

    def decrypt_secret(self, encrypted_secret: str, password: str):

        return self.MODEL_CRYPTOGRAPHY.decrypt_secret(encrypted_secret, password)

    def user_exists(self, username: str) -> bool:

        return self.MODEL_DATABASE.user_exists(username)

    def login(self, username: str, password: str) -> list:

        return self.MODEL_DATABASE.login(username, password)

    def register(self, username: str, password: str, public_key: str, private_key: str, exchange_name: str, coin_pair: str, paper_balance: str):

        self.MODEL_DATABASE.register(username, password, public_key, private_key, exchange_name, coin_pair, paper_balance)
