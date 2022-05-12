from asyncio import Event
from threading import Thread
from threading import Event as T_Event
from time import sleep
from timeit import default_timer as timer

from Account.User import Controller_User
from Exchange import Controller_Exchange_Middleware


class ModelAI(Thread):

    TIME_BETWEEN_FEE_REQUEST: float = 60.0 * 60.0 * 1.0  # Seconds * Minutes * Hours

    def __init__(self, event_main: Event, event_ai: Event, event_loop, controller_exchange_middleware: Controller_Exchange_Middleware, controller_user: Controller_User):

        Thread.__init__(self)

        self.CONTROLLER_EXCHANGE_MIDDLEWARE: Controller_Exchange_Middleware = controller_exchange_middleware
        self.CONTROLLER_USER: Controller_User = controller_user

        self.EVENT_MAIN = event_main
        self.EVENT_AI = event_ai
        self.EVENT_LOOP = event_loop

        self.event_submit_order: T_Event = T_Event()
        self.current_fee: float = 0.0
        self.current_minimum_base_order_amount: float = 0.0

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

    def __get_fee_and_min_base_order_amount(self):

        async def __get_fee_and_min_base_order_amount_async():

            self.current_fee = await self.CONTROLLER_EXCHANGE_MIDDLEWARE.get_fee()
            self.current_minimum_base_order_amount = await self.CONTROLLER_EXCHANGE_MIDDLEWARE.get_minimum_base_order_amount()
            self.event_submit_order.set()

        self.EVENT_LOOP.create_task(__get_fee_and_min_base_order_amount_async())

        self.event_submit_order.wait()
        self.event_submit_order.clear()

    def run(self) -> None:

        while self.CONTROLLER_EXCHANGE_MIDDLEWARE.get_current_price() == 0:

            if self.EVENT_MAIN.is_set():
                break
            else:
                sleep(0.001)

        s_time_fee: float = 0.0
        e_time_fee: float = self.TIME_BETWEEN_FEE_REQUEST

        while not self.EVENT_MAIN.is_set():

            if e_time_fee >= self.TIME_BETWEEN_FEE_REQUEST:

                self.__get_fee_and_min_base_order_amount()
                s_time_fee = timer()

            e_time_fee = timer() - s_time_fee

            # # # AI # # #

            print("Fee: " + str(self.current_fee))
            print("Minimum Base Order Amount: " + str(self.current_minimum_base_order_amount))
            print()

            # # # AI # # #

            sleep(0.001)

        self.EVENT_AI.set()
