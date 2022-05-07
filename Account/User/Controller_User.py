from Account.User import Model_User


class ControllerUser:

    def __init__(self, username: str, exchange_name: str, coin_pair: str, live_trading: bool):

        self.MODEL_USER = Model_User.ModelUser(username, exchange_name, coin_pair, live_trading)

    def get_username(self) -> str:

        return self.MODEL_USER.get_username()

    def get_exchange_name(self) -> str:

        return self.MODEL_USER.get_exchange_name()

    def get_coin_pair(self) -> str:

        return self.MODEL_USER.get_coin_pair()

    def is_live_trading(self) -> bool:

        return self.MODEL_USER.is_live_trading()

    def get_balance(self) -> list:

        return self.MODEL_USER.get_balance()

    def update_balance(self, base: float, quote: float):

        self.MODEL_USER.update_balance(base, quote)
