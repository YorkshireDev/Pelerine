import ccxt.async_support as ccxt
from time import sleep as pause


class ModelExchangeMiddleware:

    MAX_CONNECTION_ERROR_COUNT = 8
    MAX_CONNECTION_WAIT_MULTIPLIER = 5

    def __init__(self, **kwargs):

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

    async def load_markets(self):
        await self.__process_request(0)

    async def get_balance(self) -> list:
        return await self.__process_request(1)

    async def get_current_price(self) -> float:
        return await self.__process_request(2)

    async def submit_order(self):
        await self.__process_request(3)

    async def close_exchange(self):
        await self.__process_request(4)

    async def __process_request(self, request_id: int) -> float | list:

        connection_successful = False

        connection_error_count = 0
        connection_wait_length_multiplier = 1

        while not connection_successful:

            try:

                match request_id:

                    case 0:
                        pass
                    case 1:
                        pass
                    case 2:
                        pass
                    case 3:
                        pass
                    case 4:
                        pass

                connection_successful = True

            except (ccxt.RequestTimeout,
                    ccxt.DDoSProtection,
                    ccxt.ExchangeNotAvailable,
                    ccxt.ExchangeError,
                    ccxt.InvalidNonce) as Error:

                print("Error -> " + str(Error) + " | Retrying...")

                connection_error_count += 1
                pause(self.EXCHANGE.rateLimit * connection_wait_length_multiplier)

                if connection_wait_length_multiplier < self.MAX_CONNECTION_WAIT_MULTIPLIER:
                    if connection_error_count % self.MAX_CONNECTION_ERROR_COUNT == 0:
                        connection_wait_length_multiplier += 1
