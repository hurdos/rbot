#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os
import sys
import time
import argparse
from helper import Money, SqlAdapter
from dotenv import load_dotenv
from tinkoff.invest import Client, GetOperationsByCursorRequest, OperationState, OperationType

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--account", help="Account ID", default="2121614941") # default=ИИС
    parser.add_argument("-C", "--csv", help="Show CVS data", action="store_true")
    parser.add_argument("-U", "--update", help="Update bonds info from API", action="store_true")
    parser.add_argument("-D", "--delete", help="Delete bond by FIGI", default="")
    return parser.parse_args()

def delete_bond(figi):
    return 0

def get_bonds(account_id):   
    adp = SqlAdapter()
    token = os.getenv("TOKEN", "")
    with Client(token) as client:
        portfolio = client.operations.get_portfolio(account_id=account_id)
        for pos in portfolio.positions:
            if pos.instrument_type == 'bond':
                bond = client.instruments.bond_by(id_type=1, id=pos.figi).instrument
                (cost, coupon_payout) = get_payments(token=token, account=account_id, figi=pos.figi)
                if (adp.is_bond_exists(figi=pos.figi)):
                    adp.update_bond(figi=pos.figi, values=(pos.quantity.units, abs(cost), coupon_payout, pos.average_position_price.units, pos.current_price.units))
                    print(f"Updated: {bond.name} [{pos.figi}]")
                else:
                    adp.create_bond((pos.figi, bond.name, pos.quantity.units, bond.nominal.units, abs(cost), coupon_payout, pos.average_position_price.units, pos.current_price.units))
                    print(f"Inserted: {bond.name} [{pos.figi}]")
                time.sleep(1)
                print('-------------------------------------------------------------')
    # close sql connection
    adp.close()
    return 0

def get_payments(token="", account="", figi=""):
    with Client(token) as client:
        resp = client.operations.get_operations(account_id=account, figi=figi, state=OperationState.OPERATION_STATE_EXECUTED)
        payment = Money()
        coupon = Money()
        for operation in resp.operations:
            if operation.operation_type in (OperationType.OPERATION_TYPE_BUY, OperationType.OPERATION_TYPE_BROKER_FEE):
                payment.units += operation.payment.units
                payment.nano += operation.payment.nano
            elif operation.operation_type in (OperationType.OPERATION_TYPE_COUPON,):
                coupon.units += operation.payment.units
                coupon.nano += operation.payment.nano
    return (payment.get_amount(), coupon.get_amount())

def show_csv():
    adp = SqlAdapter()
    adp.cursor.execute('SELECT figi, name, quantity, nominal, cost, coupon_payout, avg_price, current_price FROM bonds')

    bonds = adp.cursor.fetchall()
    for bond in bonds:
        lst = []
        for item in bond:
            if type(item) is float:
                lst.append(str(item).replace('.', ','))
            else:
                lst.append(item)
        line = ';'.join(map(str, lst))
        print(line)
        # print(lst)

    # close sql connection
    adp.close()
    return 0

def show_profit():
    adp = SqlAdapter()
    adp.cursor.execute('SELECT figi, name, quantity, nominal, cost, coupon_payout FROM bonds')

    bonds = adp.cursor.fetchall()
    quantity_all = cost_all = cp_all = profit_all = nominal_all = 0
    for bond in bonds:
        # print(bond[0])
        (figi, name, quantity, nominal, cost, coupon_payout) = bond
        quantity_all += quantity
        cost_all += cost
        cp_all += coupon_payout
        nominal_sum = nominal * quantity
        nominal_all += nominal_sum
        profit = nominal_sum - cost + coupon_payout
        profit_all += profit
        precent = profit / nominal_sum * 100
        print(f"[{figi}] {name:30}[{quantity:5}] - COST:{cost:13,} | CP:{coupon_payout:10,} | PROFIT:{profit:12,.3f} | PRECENT:{precent:7.1f}%")
    
    name = 'TOTAL'
    precent = profit_all / nominal_all * 100 if nominal_all > 0 else 0
    print('-' * 131)
    print(f"{name:45}[{quantity_all:5}] - COST:{cost_all:13,.2f} | CP:{cp_all:10,} | PROFIT:{profit_all:12,.3f} | PRECENT:{precent:7.1f}%")

    # close sql connection
    adp.close()
    return 0

def main(args):
    load_dotenv()
    if args.csv:
        return show_csv()
    
    if args.update:
        return get_bonds(args.account)
    
    if args.delete:
        adp = SqlAdapter()
        adp.delete_bond(args.delete)
        adp.close()
        return 0

    show_profit()

    return 0

if __name__ == '__main__':
    args = get_args()    
    sys.exit(main(args))
