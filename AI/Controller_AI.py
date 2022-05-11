from asyncio import Event

from AI import Model_AI


class ControllerAI:

    def __init__(self, event_main: Event, event_ai: Event):

        self.MODEL_AI: Model_AI = Model_AI.ModelAI(event_main, event_ai)

    def run(self):

        self.MODEL_AI.start()
