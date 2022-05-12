import asyncio
from asyncio import Event
from threading import Thread
from getpass import getpass as secret_input
from ccxt.async_support import exchanges
from sys import exit as sys_exit

from AI import Controller_AI
from Account.Database import Controller_Database
from Account.User import Controller_User
from Exchange import Controller_Exchange_Middleware


async def login_or_register(event_loop, event_main: Event) -> dict:

    controller_database: Controller_Database = Controller_Database.ControllerDatabase()

    username: str = str(input("Username: "))
    password: str = secret_input("Password: ")
    initial_balance: list = [0.0, 0.0]

    registering: bool = False

    if controller_database.user_exists(username):  # Login

        user_information = controller_database.login(username, password)

        if len(user_information) == 0:
            print("Error -> Wrong Password Provided!")
            sys_exit()

        public_key: str = user_information[0]
        private_key: str = user_information[1]
        exchange_name = user_information[2]
        coin_pair = user_information[3]
        paper_balance = user_information[4]

        if paper_balance != "N/A":

            paper_balance_split = user_information[4].split("_")

            initial_balance[0] = float(paper_balance_split[0])
            initial_balance[1] = float(paper_balance_split[1])

        live_trading = public_key != "N/A"

    else:  # Register

        registering = True

        exchange_name = str(input("Exchange: ")).upper()
        coin_pair = str(input("Coin Pair: ")).upper()
        print()
        live_trading = str(input("Are you Live Trading or Paper Trading? (L/P): ")).upper() == "L"

        if not live_trading:

            initial_balance[1] = float(input("Starting Quote Balance: "))
            paper_balance: str = "0.0_" + str(initial_balance[1])
            print()
            public_key: str = "N/A"
            private_key: str = "N/A"

        else:

            print()
            paper_balance: str = "N/A"
            public_key: str = str(input("Public Key: "))
            private_key: str = secret_input("Private Key: ")

    controller_user: Controller_User = Controller_User.ControllerUser(username, exchange_name, coin_pair, live_trading)
    controller_user.update_balance(initial_balance[0], initial_balance[1])

    if exchange_name.lower() not in exchanges:
        print("Error -> " + exchange_name + " does not exist in CCXT!")
        sys_exit()

    controller_exchange_middleware: Controller_Exchange_Middleware = Controller_Exchange_Middleware.ControllerExchangeMiddleware(event_main,
                                                                                                                                 USER=controller_user,
                                                                                                                                 LIVE_TRADING=live_trading,
                                                                                                                                 COIN_PAIR=coin_pair,
                                                                                                                                 EXCHANGE_NAME=exchange_name,
                                                                                                                                 PUBLIC_KEY=public_key,
                                                                                                                                 PRIVATE_KEY=private_key,
                                                                                                                                 EVENT_LOOP=event_loop)

    coin_pair_exists: bool = await controller_exchange_middleware.load_markets()

    if not coin_pair_exists:
        print("Error -> " + coin_pair + " does not exist in " + exchange_name)
        await controller_exchange_middleware.close_exchange()
        sys_exit()

    if registering:
        controller_database.register(username, password, public_key, private_key, exchange_name, coin_pair, paper_balance)

    del public_key
    del private_key

    return {"USER": controller_user, "EXCHANGE": controller_exchange_middleware}


async def poll_user_balance(event_main: Event,
                            event_view: Event,
                            balance: list,
                            controller_exchange_middleware: Controller_Exchange_Middleware,
                            controller_user: Controller_User):

    seconds_passed: int = 0

    while not event_main.is_set():

        if seconds_passed % 60 == 0:

            seconds_passed = 0
            await controller_exchange_middleware.update_balance()

        temp_balance = controller_user.get_balance()
        balance[0] = temp_balance[0]
        balance[1] = temp_balance[1]

        await asyncio.sleep(1.0)
        seconds_passed += 1

    event_view.set()


async def run_ai(event_main: Event, event_view: Event, event_loop, controller_exchange_middleware: Controller_Exchange_Middleware, controller_user: Controller_User):

    event_ai = Event()

    controller_ai: Controller_AI = Controller_AI.ControllerAI(event_main, event_ai, event_loop, controller_exchange_middleware, controller_user)
    controller_ai.run()

    while not event_ai.is_set():

        await asyncio.sleep(1.0)

    event_view.set()


def poll_user_input(event_main: Event):

    input()
    event_main.set()


async def main(event_loop):

    print()

    event_main = Event()
    event_views = [Event(), Event(), Event()]  # [0] PollUserBalance, [1] PollCurrentPrice, [2] AI

    current_session = await login_or_register(event_loop, event_main)
    balance = [0.0, 0.0]

    event_loop.create_task(poll_user_balance(event_main, event_views[0], balance, current_session["EXCHANGE"], current_session["USER"]))
    event_loop.create_task(current_session["EXCHANGE"].poll_current_price(event_main, event_views[1]))
    event_loop.create_task(run_ai(event_main, event_views[2], event_loop, current_session["EXCHANGE"], current_session["USER"]))

    user_input = Thread(target=poll_user_input, args=(event_main,))
    user_input.start()

    coin_pair_split: str = current_session["USER"].get_coin_pair().split("/")

    while not event_main.is_set():

        current_user_str: str = str(current_session["USER"].get_username())
        exchange_name_str: str = str(current_session["USER"].get_exchange_name())
        coin_pair_str: str = str(current_session["USER"].get_coin_pair())
        live_trading_str: str = str(current_session["USER"].is_live_trading())
        current_price_str: str = str(current_session["EXCHANGE"].get_current_price())
        balance_str: str = str(balance[0]) + " " + coin_pair_split[0] + " | " + str(balance[1]) + " " + coin_pair_split[1]

        print(f"Current User: {current_user_str}\n"
              f"Exchange Name: {exchange_name_str}\n"
              f"Coin Pair: {coin_pair_str}\n"
              f"Live Trading: {live_trading_str}\n"
              f"Current Price: {current_price_str}\n"
              f"Current Balance: {balance_str}\n")

        await asyncio.sleep(1.0)

    for event_view in event_views:
        await event_view.wait()

    await current_session["EXCHANGE"].close_exchange()

    print()
