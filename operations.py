#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os
import sys
import argparse
from dotenv import load_dotenv
from tinkoff.invest import Client, GetOperationsByCursorRequest, OperationType

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--instrument", help="Instrument id/uid or figi", default="")
    parser.add_argument("-S", "--sum", help="Sum of operations", action="store_true")
    return parser.parse_args()
    
def print_operations (operations):
    op = operations.items[0]
    dt = op.date.strftime('%d-%m-%Y %H:%M:%S %Z')
    payment = str(op.payment.units) + ',' + str(abs(op.payment.nano)) + ' ' + op.payment.currency
    commission = str(op.commission.units) + ',' + str(abs(op.commission.nano)) + ' ' + op.commission.currency
    print (f"{dt} - [{op.type}] {op.name}: {op.description} | {payment} | {commission:30} | [{op.figi}] [{op.instrument_uid}] ")
    return 0
    
def get_request(cursor="", account="", instrument="", limit=1):
    return GetOperationsByCursorRequest(
        account_id=account,
        instrument_id=instrument,
        cursor=cursor,
        limit=limit,
        without_commissions=True,
    )
    
def show_operations(token="", account="", instrument=""):
    with Client(token) as client:
        operations = client.operations.get_operations_by_cursor(get_request(account=account, instrument=instrument))
        print_operations(operations)
        while operations.has_next:
            request = get_request(cursor=operations.next_cursor, account=account, instrument=instrument)
            operations = client.operations.get_operations_by_cursor(request)
            print_operations(operations)
            
def sum_operations(token="", account="", instrument=""):
    with Client(token) as client:
        operations = client.operations.get_operations_by_cursor(get_request(account=account, instrument=instrument, limit=100))
        #print(operations.items[0])
        name = operations.items[0].name
        buy_sum_units = buy_sum_nano = 0
        coupon_sum_units = coupon_sum_nano = 0
        for item in operations.items:
            if item.type == OperationType.OPERATION_TYPE_BUY:
                buy_sum_units += item.payment.units + item.commission.units
                buy_sum_nano += item.payment.nano + item.commission.nano
            elif item.type == OperationType.OPERATION_TYPE_COUPON:
                coupon_sum_units += item.payment.units + item.commission.units
                coupon_sum_nano += item.payment.nano + item.commission.nano
                
        #print(buy_sum_units, buy_sum_nano)
        #print(coupon_sum_units, coupon_sum_nano)
        buy_sum = buy_sum_units + buy_sum_nano/10000000000
        coupon_sum = coupon_sum_units + coupon_sum_nano/10000000000
        print("Наименование | Сумма покупки | Сумма выплат по купонам | Сумма покупки за вычетом купонов")
        print(f"{name} | {buy_sum} | {coupon_sum} | {buy_sum + coupon_sum}")

def main(args):
    load_dotenv()
    token = os.getenv("TOKEN", "")
    account_id = os.getenv("ACCOUNT_ID", "")
    instrument_id = args.instrument
    
    if args.sum and instrument_id != "":
        sum_operations(token=token, account=account_id, instrument=instrument_id)
    else:
        show_operations(token=token, account=account_id, instrument=instrument_id)
    
    return 0

if __name__ == '__main__':    
    args = get_args()
    sys.exit(main(args))
