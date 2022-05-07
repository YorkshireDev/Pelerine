from sys import argv
from platform import system as operating_system
import asyncio

from View import View_Headless
from View import View_Graphical

if __name__ == "__main__":

    USER_INTERFACE = None

    if len(argv) > 1:
        USER_INTERFACE = View_Headless
    else:
        USER_INTERFACE = View_Graphical

    if operating_system().upper() == "WINDOWS":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    EVENT_LOOP = asyncio.new_event_loop()
    EVENT_LOOP.run_until_complete(USER_INTERFACE.main())
