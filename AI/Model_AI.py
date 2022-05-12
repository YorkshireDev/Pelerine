from asyncio import Event
from threading import Thread
from threading import Event as T_Event
from time import sleep

from Account.User import Controller_User
from Exchange import Controller_Exchange_Middleware


class ModelAI(Thread):

    def __init__(self, event_main: Event, event_ai: Event, event_loop, controller_exchange_middleware: Controller_Exchange_Middleware, controller_user: Controller_User):

        Thread.__init__(self)

        self.CONTROLLER_EXCHANGE_MIDDLEWARE: Controller_Exchange_Middleware = controller_exchange_middleware
        self.CONTROLLER_USER: Controller_User = controller_user

        self.EVENT_MAIN = event_main
        self.EVENT_AI = event_ai
        self.EVENT_LOOP = event_loop

        self.event_submit_order: T_Event = T_Event()

    def __buy(self, amount: float):

        async def __buy_async(x: float):

            await self.CONTROLLER_EXCHANGE_MIDDLEWARE.submit_order(True, x)
            self.event_submit_order.set()

        self.EVENT_LOOP.create_task(__buy_async(amount))

        self.event_submit_order.wait()
        self.event_submit_order.clear()

    def __sell(self, amount: float):

        async def __sell_async(x: float):

            await self.CONTROLLER_EXCHANGE_MIDDLEWARE.submit_order(False, x)
            self.event_submit_order.set()

        self.EVENT_LOOP.create_task(__sell_async(amount))

        self.event_submit_order.wait()
        self.event_submit_order.clear()

    def run(self) -> None:

        while self.CONTROLLER_EXCHANGE_MIDDLEWARE.get_current_price() == 0:

            if self.EVENT_MAIN.is_set():
                break
            else:
                sleep(0.001)

        buying_price: float = 0.0

        while not self.EVENT_MAIN.is_set():

            self.__buy(self.CONTROLLER_USER.get_balance()[1] / 8.0)

            buying_price = self.CONTROLLER_EXCHANGE_MIDDLEWARE.get_current_price()

            while self.CONTROLLER_EXCHANGE_MIDDLEWARE.get_current_price() <= buying_price:

                if self.EVENT_MAIN.is_set():
                    break
                else:
                    sleep(0.001)

            self.__sell(self.CONTROLLER_USER.get_balance()[0])

            sleep(5.0)

        self.EVENT_AI.set()
