from asyncio import Event

from AI import Model_AI
from Exchange import Controller_Exchange_Middleware


class ControllerAI:

    def __init__(self, event_main: Event, event_ai: Event, controller_exchange_middleware: Controller_Exchange_Middleware):

        self.MODEL_AI: Model_AI = Model_AI.ModelAI(event_main, event_ai, controller_exchange_middleware)

    def run(self):

        self.MODEL_AI.start()
