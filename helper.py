
import sqlite3

class Money():
    units: int = 0
    nano: int = 0

    def get_amount(self):
        return self.units + self.nano/1000000000

class SqlAdapter():
    conn = None
    cursor = None
    def __init__(self):
        self.conn = sqlite3.connect('invest.db3')
        self.cursor = self.conn.cursor()
        # create table bonds
        self.cursor.execute('''
        CREATE TABLE IF NOT EXISTS "bonds" (
            "figi"	TEXT NOT NULL UNIQUE,
            "name"	TEXT,
            "quantity"	INTEGER NOT NULL,
            "nominal"	INTEGER NOT NULL,
            "cost"	NUMERIC NOT NULL,
            "coupon_payout"	NUMERIC NOT NULL,
            "avg_price"	INTEGER NOT NULL,
            "current_price"	INTEGER NOT NULL,
            PRIMARY KEY("figi")
        )
        ''')
        self.conn.commit()

    def is_bond_exists(self, figi=''):
        self.cursor.execute('SELECT figi FROM bonds WHERE figi = ?', (figi,))
        res = self.cursor.fetchone()
        # print(res)
        return bool(res)
    
    def create_bond(self, values=()):
        # print('figi, name, quantity, nominal, cost, coupon_payout, avg_price, current_price')
        # print(values)
        self.cursor.execute('INSERT INTO bonds (figi, name, quantity, nominal, cost, coupon_payout, avg_price, current_price) VALUES (?, ?, ?, ?, ?, ?, ?, ?)', values)
        self.conn.commit()

    def update_bond(self, figi='', values=()):
        # print(figi)
        # print('quantity, cost, coupon_payout, avg_price, current_price')
        # print(values)
        values = values + (figi,)
        # print(values)
        self.cursor.execute('UPDATE bonds SET quantity = ?, cost = ?, coupon_payout = ?, avg_price = ?, current_price = ? WHERE figi = ?', values)
        self.conn.commit()

    def delete_bond(self, figi=''):
        # print(figi)
        self.cursor.execute('DELETE FROM bonds WHERE figi = ?', (figi,))
        # print(self.cursor.rowcount)
        self.conn.commit()

    def close(self):
        self.conn.close()