from asyncio import Event
from threading import Thread
from threading import Event as T_Event
from time import sleep
from timeit import default_timer as timer

from Account.User import Controller_User
from Exchange import Controller_Exchange_Middleware


class ModelAI(Thread):

    TIME_BETWEEN_FEE_REQUEST: float = 60.0 * 60.0 * 1.0  # Seconds * Minutes * Hours

    MAX_GRID_AMOUNT: int = 128
    GRID_PRICE_COVERAGE: float = 10.0 / 100.0  # 10%

    def __init__(self, event_main: Event, event_ai: Event, event_loop, controller_exchange_middleware: Controller_Exchange_Middleware, controller_user: Controller_User):

        Thread.__init__(self)

        self.CONTROLLER_EXCHANGE_MIDDLEWARE: Controller_Exchange_Middleware = controller_exchange_middleware
        self.CONTROLLER_USER: Controller_User = controller_user

        self.EVENT_MAIN = event_main
        self.EVENT_AI = event_ai
        self.EVENT_LOOP = event_loop

        self.event_submit_order: T_Event = T_Event()

        self.current_fee: float = 0.0
        self.current_minimum_base_order_amount: float = 0.0  # Minimum BASE purchasable by the exchange
        self.current_base_order_amount: float = 0.0  # The amount of BASE the AI will buy, always >= minimum base order amount

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

    def __calculate_grid_structure(self) -> dict:

        quote_balance: float = self.CONTROLLER_USER.get_balance()[1] * 0.95
        current_price = self.CONTROLLER_EXCHANGE_MIDDLEWARE.get_current_price()

        grid_amount: int = int(((quote_balance / current_price) // self.current_minimum_base_order_amount))
        self.current_base_order_amount = self.current_minimum_base_order_amount

        if grid_amount > self.MAX_GRID_AMOUNT:

            self.current_base_order_amount *= (grid_amount / self.MAX_GRID_AMOUNT)
            grid_amount = self.MAX_GRID_AMOUNT

        grid_separation_percentage: float = self.GRID_PRICE_COVERAGE / grid_amount
        grid_separation_value: float = current_price * grid_separation_percentage

        sell_grid = (current_price + grid_separation_value) * (1.0 + self.current_fee)

        buy_grid_structure: list = []  # [ [PRICE, BOUGHT?], [PRICE, BOUGHT?], .. ]

        for _ in range(grid_amount):

            current_price -= grid_separation_value
            buy_grid_structure.append([current_price * (1.0 - self.current_fee), False])
            print("Buy: " + str(buy_grid_structure[-1][0]))

        print("Sell: " + str(sell_grid))

        return {"BUY": buy_grid_structure, "SELL": sell_grid}

    def __determine_buy(self, current_price: float, buy_grid_structure: list) -> bool:

        return False

    def __determine_sell(self, current_price: float, sell_grid_price: float) -> bool:

        return False

    def run(self) -> None:

        while self.CONTROLLER_EXCHANGE_MIDDLEWARE.get_current_price() == 0:

            if self.EVENT_MAIN.is_set():
                break
            else:
                sleep(0.001)

        self.__get_fee_and_min_base_order_amount()
        grid_structure: dict = self.__calculate_grid_structure()

        s_time: float = timer()
        e_time: float = 0.0

        while not self.EVENT_MAIN.is_set():

            if e_time >= self.TIME_BETWEEN_FEE_REQUEST:

                self.__get_fee_and_min_base_order_amount()
                s_time = timer()

            e_time = timer() - s_time

            # # # AI # # #

            current_price: float = self.CONTROLLER_EXCHANGE_MIDDLEWARE.get_current_price()

            if self.__determine_buy(current_price, grid_structure["BUY"]):

                self.__buy(self.current_base_order_amount)

            elif self.__determine_sell(current_price, grid_structure["SELL"]):

                self.__sell(self.CONTROLLER_USER.get_balance()[0])

            # # # AI # # #

            sleep(0.001)

        self.EVENT_AI.set()
