# Write your code here
import sqlite3
from random import randint


class Banking:

    def __init__(self):
        self.id = ''
        self.card = ''
        self.pin = ''
        self.balance = ''
        self.conn = sqlite3.connect('card.s3db')
        self.cur = self.conn.cursor()
        self.init_db()

        self.menu_logout()

    def close_db(self):
        try:
            self.conn.close()
        except Exception as e:
            print(e)

    def commit_db(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
        except Exception as e:
            print(e)

    def fetchone_db(self, sql):
        try:
            self.cur.execute(sql)
            return self.cur.fetchone()
        except Exception as e:
            print(e)

    def init_db(self):
        sql_create = 'CREATE TABLE IF NOT EXISTS card (' \
                     '   id INTEGER PRIMARY KEY AUTOINCREMENT, ' \
                     '   number TEXT, ' \
                     '   pin TEXT, ' \
                     '   balance INTEGER DEFAULT 0' \
                     ');'
        self.commit_db(sql_create)

    def create_account(self):
        card = '400000{:09}'.format(randint(0, 999999999))
        s = 0
        for i in range(0, 15):
            n = int(card[i])
            n *= 2 if (i + 1) % 2 == 1 else 1
            n -= 9 if n > 9 else 0
            s += n

        cs = 0 if s % 10 == 0 else 10 - s % 10

        self.card = card + str(cs)
        self.pin = '{:04}'.format(randint(0, 9999))
        self.balance = 0

        sql = f"INSERT INTO card (number, pin) " \
              f"VALUES ({self.card}, {self.pin})" \
              f";"

        self.commit_db(sql)

        print(f'Your card has been created\n'
              f'Your card number:\n{self.card}\n'
              f'Your card PIN:\n{self.pin}')

        self.menu_logout()

    def login(self, card, pin):

        sql_login = f"SELECT * FROM card " \
                    f"WHERE number = {card} and pin = {pin};"
        res = self.fetchone_db(sql_login)
        if res:
            print('You have successfully logged in!')
            self.id = res[0]
            self.card = card
            self.pin = pin
            self.balance = res[3]
            return True
        else:
            print('Wrong card number or PIN!')
            return False

    def logout(self):
        self.menu_logout()

    def get_balance(self):
        print(f'Balance: {self.balance}')
        self.menu_login()

    def add_income(self):
        income = int(input('Enter income:\n'))

        self.balance = str(income + int(self.balance))
        sql_update = f"UPDATE card SET balance = {self.balance} " \
                     f"WHERE number = {self.card} and pin = {self.pin};"
        self.commit_db(sql_update)

        print('Income was added!')
        self.menu_login()

    def transfer(self):
        to_n = input('Enter card number:\n')

        s = 0
        for i in range(0, 15):
            n = int(to_n[i])
            n *= 2 if (i + 1) % 2 == 1 else 1
            n -= 9 if n > 9 else 0
            s += n

        if (int(to_n[-1]) == 0 and s % 10 == 0) or (int(to_n[-1]) == 10 - s % 10):
            sql = f"SELECT * FROM card WHERE number = {to_n};"

            to_account = self.fetchone_db(sql)
            if to_account:
                amount = int(input('Enter how much money you want to transfer:'))
                if amount > int(self.balance):
                    print('Not enough money!')
                else:
                    sql_update_from = f'UPDATE card SET balance = {str(int(self.balance) - amount)} ' \
                                      f'WHERE number = {self.card} and pin = {self.pin};'
                    self.commit_db(sql_update_from)
                    sql_update_to = f'UPDATE card SET balance = {str(int(to_account[3]) + amount)} ' \
                                    f'WHERE number = {to_account[1]} and pin = {to_account[2]};'
                    self.commit_db(sql_update_to)

            else:
                print('Such a card does not exist.')
        else:
            print('Probably you made a mistake in the card number. Please try again!')

        self.menu_login()

    def close_account(self):
        sql_close = f'Delete FROM card WHERE number = {self.card} and pin = {self.pin};'
        self.commit_db(sql_close)
        print('The account has been closed!')
        self.menu_logout()

    def menu_logout(self):
        opt = input('1. Create an account\n'
                    '2. Log into account\n'
                    '0. Exit\n')

        if opt == '1':
            self.create_account()

        elif opt == '2':
            card = input('Enter your card number:\n')
            pin = input('Enter your PIN:\n')

            if self.login(card, pin):
                self.menu_login()
            else:
                self.menu_logout()

        elif opt == '0':
            print('Bye!')
            exit()

    def menu_login(self):
        opt = input('1. Balance\n'
                    '2. Add income\n'
                    '3. Do transfer\n'
                    '4. Close account\n'
                    '5. Log out\n'
                    '0. Exit\n')

        if opt == '1':
            self.get_balance()
        elif opt == '2':
            self.add_income()
        elif opt == '3':
            self.transfer()
        elif opt == '4':
            self.close_account()
        elif opt == '5':
            self.logout()
        elif opt == '0':
            print('Bye!')
            exit()


banking = Banking()
