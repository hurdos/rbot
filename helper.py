
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

    def close(self):
        self.conn.close()