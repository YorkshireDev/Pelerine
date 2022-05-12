import ccxt.async_support as ccxt
from asyncio import sleep as pause
from asyncio import Event

from Account.User import Controller_User


class ModelExchangeMiddleware:

    MAX_CONNECTION_ERROR_COUNT = 8
    MAX_CONNECTION_WAIT_MULTIPLIER = 5

    def __init__(self, event_main: Event, **kwargs):

        self.EVENT_MAIN: Event = event_main

        self.CONTROLLER_USER: Controller_User = kwargs["USER"]

        self.LIVE_TRADING: bool = kwargs["LIVE_TRADING"]
        self.COIN_PAIR: str = kwargs["COIN_PAIR"]

        self.EXCHANGE = getattr(ccxt, kwargs["EXCHANGE_NAME"].lower())

        if self.LIVE_TRADING:

            self.EXCHANGE = self.EXCHANGE({"verbose": False,
                                           "enableRateLimit": True,
                                           "asyncio_loop": kwargs["EVENT_LOOP"],
                                           "apiKey": kwargs["PUBLIC_KEY"],
                                           "secret": kwargs["PRIVATE_KEY"]})

        else:

            self.EXCHANGE = self.EXCHANGE({"verbose": False,
                                           "enableRateLimit": True,
                                           "asyncio_loop": kwargs["EVENT_LOOP"]})

        self.current_price: float = 0.0

    async def load_markets(self) -> bool:

        await self.__process_request(0, False)
        return self.COIN_PAIR in self.EXCHANGE.symbols

    async def update_balance(self, **kwargs):

        await self.__process_request(1, False, **kwargs)

    async def get_current_price(self) -> float:

        await self.__process_request(2, False)
        return self.current_price

    async def submit_order(self, side: bool, amount: float):

        return await self.__process_request(3, True, SIDE=side, AMOUNT=amount)

    async def close_exchange(self):

        await self.__process_request(4, True)

    async def __process_request(self, request_id: int, no_retry: bool, **kwargs) -> bool:

        connection_successful = False

        connection_error_count = 0
        connection_wait_length_multiplier = 1
        pause_length = self.EXCHANGE.rateLimit * 0.001

        while not connection_successful:

            try:

                match request_id:

                    case 0:

                        await self.EXCHANGE.load_markets(True)

                    case 1:

                        base: float = 0.0
                        quote: float = 0.0

                        if self.LIVE_TRADING:

                            coin_pair_split = self.COIN_PAIR.split("/")

                            account_balances: dict = await self.EXCHANGE.fetch_balance()
                            account_balances = account_balances["total"]

                            if coin_pair_split[0] in account_balances:
                                base = float(account_balances[coin_pair_split[0]])

                            if coin_pair_split[1] in account_balances:
                                quote = float(account_balances[coin_pair_split[1]])

                        else:

                            if len(kwargs) == 0:

                                base = self.CONTROLLER_USER.get_balance()[0]
                                quote = self.CONTROLLER_USER.get_balance()[1]

                            else:

                                base = float(kwargs["BASE"])
                                quote = float(kwargs["QUOTE"])

                        self.CONTROLLER_USER.update_balance(base, quote)

                    case 2:

                        temp_current_price = await self.EXCHANGE.fetch_ticker(self.COIN_PAIR)
                        self.current_price = float(temp_current_price["last"])

                    case 3:

                        side: bool = bool(kwargs["SIDE"])
                        amount: float = float(kwargs["AMOUNT"])

                        if side:  # Buy

                            if self.LIVE_TRADING:

                                pass

                            else:

                                user_balance = self.CONTROLLER_USER.get_balance()

                                base_amount: float = amount / self.current_price

                                base: float = user_balance[0] + base_amount
                                quote: float = user_balance[1] - amount

                                await self.update_balance(BASE=base, QUOTE=quote)

                        else:  # Sell

                            if self.LIVE_TRADING:

                                pass

                            else:

                                pass


                    case 4:

                        await self.EXCHANGE.close()

                connection_successful = True

            except (ccxt.RequestTimeout,
                    ccxt.DDoSProtection,
                    ccxt.ExchangeNotAvailable,
                    ccxt.ExchangeError,
                    ccxt.InvalidNonce) as Error:

                if no_retry:
                    print("Error -> " + str(Error) + " | Abandoning...")
                    return False

                if self.EVENT_MAIN.is_set():
                    return False

                print("Error -> " + str(Error) + " | Retrying...")

                connection_error_count += 1

                await pause(pause_length)

                if connection_wait_length_multiplier < self.MAX_CONNECTION_WAIT_MULTIPLIER:
                    if connection_error_count % self.MAX_CONNECTION_ERROR_COUNT == 0:
                        connection_wait_length_multiplier += 1
                        pause_length = (self.EXCHANGE.rateLimit * 0.001) * connection_wait_length_multiplier

        return True
