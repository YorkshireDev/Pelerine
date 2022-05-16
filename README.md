# Pelerine
Project Pelerine

---

## Summary

Pelerine is a free and open-source (FOSS) autonomous cryptocurrency trading bot made entirely with Python, using the copyleft GPL v3.0 license, that is also cross-platform and lightweight on system resources.

---

## Features (Current)

* Live Trading - Input API keys from FTX and let the bot trade.

* Paper Trading - Want to test it out? A paper trading mode (fake money) is implemented and otherwise works identically to the live trader.

* Persistence - Accounts are stored in a local SQLite database, your private API key is protected with encryption and your password is strongly hashed and salted.

* Full automation - The AI is a grid trading bot. Everything you would have to configure on a trading exchange: grid amounts; grid separation, profit percentage; safety orders; and more are all done for you. All you need to do is set-and-forget. The AI will follow the price of a coin pair up or down over time to trade as often as possible!

* Ease-of-use - All you have to do is register or login and the bot will automatically start running.

* Real-time reporting - The current price of a coin-pair, your balance from your exchange and the percentage profit made since the bot started is all reported in real-time.

* Modular code - If you wanted to write your own AI from scratch, the only requirement is that it is initialised by the AI controller and inherits the Thread package.

---

## Features (Upcoming)

* Any exchange - Currently limited to FTX, the aim is to allow most of the exchanges supported by [CCXT](https://github.com/ccxt/ccxt) - which is the library used for connecting to exchanges.

* Customisable parameters - The grid amount, price coverage and timings are currently non-customisable, so advanced users will be able to customise those out-of-code if they wished, while non-advanced users can just leave them be.

* Graphical User Interface (GUI) - A GUI is planned to be created after the core functionality of the program is finished.

---

## Requirements & Setup

1. Python **3.10** or later is required.

2. Windows (Tested in Windows 10 21H2), Linux (Tested in Ubuntu 22.04 LTS, Raspberry Pi 4 with Pi-OS Lite **64-bit**) or macOS (Untested)

3. Open up a Terminal/Powershell/Whatever in the directory of Pelerine.

4. You can use Python system-wide, but it is recommended to [create a Virtual Environment](https://realpython.com/python-virtual-environments-a-primer/#create-it).

5. In the root directory there is a text file called requirements.txt, to install the packages type `pip install -r requirements.txt`

6.
   1. To start the headless version, type `Python Main.py -H`
   2. To start the GUI version, type `Python Main.py`, or in Windows you can usually just double-click the Main.py file.


---

## Usage

When you start the program, you will be asked to type in some initial things, brackets indicate in what context they will appear:

* Username (Login/Register): The username of this "account".
* Password (Login/Register): The password of this "account" (make it very secure!).
* Exchange (Register): The exchange you want to connect to.
* Coin Pair (Register): The coin pair you want to trade (e.g., ETH/BTC, ALGO/USDT, etc. See your exchange for supported currencies!)
* Are you Live Trading or Paper Trading? (Register): Type L for Live Trading, type P for Paper Trading.
* Public Key (Register/Live): The public key from your exchange.
* Private Key (Register/Live): The private key from your exchange.
* Starting Quote Balance (Register/Paper): The starting quote currency balance for your paper trading account.
