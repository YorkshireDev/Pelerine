from getpass import getpass as secret_input

from Account.Database import Controller_Database
from Account.User import Controller_User


def login_or_register() -> dict:

    controller_database: Controller_Database = Controller_Database.ControllerDatabase()

    username: str = str(input("Username: "))
    password: str = secret_input("Password: ")
    initial_balance: list = [0.0, 0.0]

    if controller_database.user_exists(username):  # Login

        user_information = controller_database.login(username, password)

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

        controller_database.register(username, password, public_key, private_key, exchange_name, coin_pair, paper_balance)

    controller_user: Controller_User = Controller_User.ControllerUser(username, exchange_name, coin_pair, live_trading)
    controller_user.update_balance(initial_balance[0], initial_balance[1])

    print("Public Key: " + public_key)
    print("Private Key: " + private_key)

    return {"USER": controller_user, "EXCHANGE": None}


async def main():

    print()

    current_user = login_or_register()

    print("Username: " + current_user["USER"].get_username())
    print("Exchange Name: " + current_user["USER"].get_exchange_name())
    print("Coin Pair: " + current_user["USER"].get_coin_pair())
    print("Live Trading: " + str(current_user["USER"].is_live_trading()))
    print("Balance: " + str(current_user["USER"].get_balance()))

    print()
