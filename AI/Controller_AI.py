from asyncio import Event

from AI import Model_AI
from Account.User import Controller_User
from Exchange import Controller_Exchange_Middleware


class ControllerAI:

    def __init__(self, event_main: Event, event_ai: Event, event_loop, controller_exchange_middleware: Controller_Exchange_Middleware, controller_user: Controller_User):

        self.MODEL_AI: Model_AI = Model_AI.ModelAI(event_main, event_ai, event_loop, controller_exchange_middleware, controller_user)

    def run(self):

        self.MODEL_AI.start()
