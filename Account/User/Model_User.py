class ModelUser:

    def __init__(self, username: str, exchange_name: str, coin_pair: str, live_trading: bool):

        self.USERNAME: str = username
        self.EXCHANGE_NAME: str = exchange_name
        self.COIN_PAIR: str = coin_pair
        self.LIVE_TRADING: bool = live_trading

        self.balance: list = [0.0, 0.0]

    def get_username(self) -> str:

        return self.USERNAME

    def get_exchange_name(self) -> str:

        return self.EXCHANGE_NAME

    def get_coin_pair(self) -> str:

        return self.COIN_PAIR

    def is_live_trading(self) -> bool:

        return self.LIVE_TRADING

    def get_balance(self) -> list:

        return self.balance

    def update_balance(self, base: int, quote: int):

        self.balance[0] = base
        self.balance[1] = quote
