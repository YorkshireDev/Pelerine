import asyncio
from asyncio import Event

from Exchange import Model_Exchange_Middleware


class ControllerExchangeMiddleware:

    def __init__(self, event_main: Event, **kwargs):

        self.MODEL_EXCHANGE_MIDDLEWARE: Model_Exchange_Middleware = Model_Exchange_Middleware.ModelExchangeMiddleware(event_main, **kwargs)
        self.current_price: float = 0.0

    def get_profit_percentage(self) -> str:

        return self.MODEL_EXCHANGE_MIDDLEWARE.get_profit_percentage()

    async def poll_current_price(self, event_main: Event, event_view: Event):

        while not event_main.is_set():

            self.current_price = await self.__get_current_price()
            await asyncio.sleep(0.001)

        event_view.set()

    async def load_markets(self) -> bool:

        return await self.MODEL_EXCHANGE_MIDDLEWARE.load_markets()

    async def update_balance(self, **kwargs):

        await self.MODEL_EXCHANGE_MIDDLEWARE.update_balance(**kwargs)

    async def __get_current_price(self) -> float:

        return await self.MODEL_EXCHANGE_MIDDLEWARE.get_current_price()

    def get_current_price(self) -> float:

        return self.current_price

    async def submit_order(self, side: bool, amount: float, safety_order: bool = False) -> bool:

        success: bool = await self.MODEL_EXCHANGE_MIDDLEWARE.submit_order(side, amount, safety_order)
        return success

    async def close_exchange(self):

        await self.MODEL_EXCHANGE_MIDDLEWARE.close_exchange()

    async def get_fee(self) -> float:

        return await self.MODEL_EXCHANGE_MIDDLEWARE.get_fee()

    async def get_minimum_base_order_amount(self) -> float:

        return await self.MODEL_EXCHANGE_MIDDLEWARE.get_minimum_base_order_amount()
