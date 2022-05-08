import ccxt.async_support as ccxt
from time import sleep as pause


class ModelExchangeMiddleware:

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
        pass
