import sqlite3 as dbms
from sqlite3 import Error

from Account.Database import Controller_Database


class ModelDatabase:

    def __init__(self, controller_database: Controller_Database.ControllerDatabase):

        self.CONTROLLER_DATABASE = controller_database
        self.CONNECTION = None

        try:

            self.CONNECTION = dbms.connect("Users.db")

            if self.CONNECTION is not None:

                query = """ CREATE TABLE IF NOT EXISTS users
                 (
                 id integer PRIMARY KEY,
                 username text NOT NULL,
                 password text NOT NULL,
                 public_key text NOT NULL,
                 private_key text NOT NULL
                 ); """

                cursor = self.CONNECTION.cursor()
                cursor.execute(query)

        except Error as error:
            print(str(error))

    def user_exists(self, username: str) -> bool:

        query = """ SELECT id FROM users WHERE username=? """

        try:

            cursor = self.CONNECTION.cursor()
            cursor.execute(query, (username,))

            return len(cursor.fetchall()) > 0

        except Error as error:
            print(str(error))

    def login(self, username: str, password: str) -> list:

        query = """ SELECT password,public_key,private_key FROM users WHERE username=? """

        try:

            cursor = self.CONNECTION.cursor()
            cursor.execute(query, (username,))

            request = cursor.fetchone()

            if self.CONTROLLER_DATABASE.verify_hash(request[0], password):
                return [request[1], self.CONTROLLER_DATABASE.decrypt_secret(request[2], password)]
            else:
                return []

        except Error as error:
            print(str(error))

    def register(self, username: str, password: str, public_key: str, private_key: str):

        query = """ INSERT INTO users(username,password,public_key,private_key) VALUES(?,?,?,?) """

        try:

            cursor = self.CONNECTION.cursor()
            cursor.execute(query, (username,
                                   self.CONTROLLER_DATABASE.get_hash(password),
                                   public_key,
                                   self.CONTROLLER_DATABASE.encrypt_secret(private_key, password)))

            self.CONNECTION.commit()

        except Error as error:
            print(str(error))
