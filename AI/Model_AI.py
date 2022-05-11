from asyncio import Event
from threading import Thread


class ModelAI(Thread):

    def __init__(self, event_main: Event, event_ai: Event):

        Thread.__init__(self)

        self.EVENT_MAIN = event_main
        self.EVENT_AI = event_ai

    def run(self) -> None:

        i: int = 0

        while not self.EVENT_MAIN.is_set():
            i += 1

        self.EVENT_AI.set()
