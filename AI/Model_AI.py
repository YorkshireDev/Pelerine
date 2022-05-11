from asyncio import Event
from threading import Thread

from Exchange import Controller_Exchange_Middleware


class ModelAI(Thread):

    def __init__(self, event_main: Event, event_ai: Event, controller_exchange_middleware: Controller_Exchange_Middleware):

        Thread.__init__(self)

        self.CONTROLLER_EXCHANGE_MIDDLEWARE: Controller_Exchange_Middleware = controller_exchange_middleware

        self.EVENT_MAIN = event_main
        self.EVENT_AI = event_ai

    def run(self) -> None:

        while not self.EVENT_MAIN.is_set():

            current_price: int = self.CONTROLLER_EXCHANGE_MIDDLEWARE.get_current_price()

        self.EVENT_AI.set()
