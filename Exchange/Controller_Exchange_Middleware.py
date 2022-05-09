from asyncio import Event

from Exchange import Model_Exchange_Middleware


class ControllerExchangeMiddleware:

    def __init__(self, event_main: Event, **kwargs):

        self.MODEL_EXCHANGE_MIDDLEWARE: Model_Exchange_Middleware = Model_Exchange_Middleware.ModelExchangeMiddleware(event_main, **kwargs)

    async def load_markets(self) -> bool:

        return await self.MODEL_EXCHANGE_MIDDLEWARE.load_markets()

    async def update_balance(self):

        await self.MODEL_EXCHANGE_MIDDLEWARE.update_balance()

    async def get_current_price(self) -> float:

        return await self.MODEL_EXCHANGE_MIDDLEWARE.get_current_price()

    async def submit_order(self):

        await self.MODEL_EXCHANGE_MIDDLEWARE.submit_order()

    async def close_exchange(self):

        await self.MODEL_EXCHANGE_MIDDLEWARE.close_exchange()
