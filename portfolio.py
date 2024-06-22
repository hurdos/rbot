#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os
import sys
import argparse
from dotenv import load_dotenv
from tinkoff.invest import Client

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--account", help="Account ID", default="2121614941") # default=ИИС
    return parser.parse_args()

def show_money (money):
    value = money.units + money.nano/10000000000
    return str(value) + " " + money.currency

def show_position(pos):
    average_position_price = show_money(pos.average_position_price)
    current_price = show_money(pos.current_price)
    print(f"{pos.figi} | {pos.instrument_type:10} | {pos.quantity.units:5} | {average_position_price:>12} | {current_price:>12}")

def main(args):
    load_dotenv()
    token = os.getenv("TOKEN", "")
    #account_id = os.getenv("ACCOUNT_ID", "")
    account_id = args.account
    
    with Client(token) as client:
        #positions = client.operations.get_positions(account_id=account_id)
        #print(positions)
        portfolio = client.operations.get_portfolio(account_id=account_id)
        print(f"Сумма на Балансе: {show_money(portfolio.total_amount_currencies)}")
        print(f"Общая сумма по акциям: {show_money(portfolio.total_amount_shares)}")
        print(f"Общая сумма по облигациям: {show_money(portfolio.total_amount_bonds)}")
        print("-"*65)
        for pos in portfolio.positions:
            show_position(pos)
    return 0

if __name__ == '__main__':
    args = get_args()
    sys.exit(main(args))
