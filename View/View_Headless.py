from getpass import getpass as secret_input
from ccxt.async_support import exchanges
from sys import exit as sys_exit

from Account.Database import Controller_Database
from Account.User import Controller_User
from Exchange import Controller_Exchange_Middleware


async def login_or_register(event_loop) -> dict:

    controller_database: Controller_Database = Controller_Database.ControllerDatabase()

    username: str = str(input("Username: "))
    password: str = secret_input("Password: ")
    initial_balance: list = [0.0, 0.0]

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

    controller_exchange_middleware: Controller_Exchange_Middleware = Controller_Exchange_Middleware.ControllerExchangeMiddleware(USER=controller_user,
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

    controller_database.register(username, password, public_key, private_key, exchange_name, coin_pair, paper_balance)

    return {"USER": controller_user, "EXCHANGE": controller_exchange_middleware}


async def main(event_loop):

    print()

    current_session = await login_or_register(event_loop)

    await current_session["EXCHANGE"].update_balance()
    print("Current Price: " + str(await current_session["EXCHANGE"].get_current_price()))

    print()

    print("Username: " + str(current_session["USER"].get_username()))
    print("Exchange Name: " + str(current_session["USER"].get_exchange_name()))
    print("Coin Pair: " + str(current_session["USER"].get_coin_pair()))
    print("Live Trading: " + str(current_session["USER"].is_live_trading()))
    print("Balance: " + str(current_session["USER"].get_balance()))

    await current_session["EXCHANGE"].close_exchange()

    print()
