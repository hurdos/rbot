#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import os, sys
from dotenv import load_dotenv
from datetime import date
from tinkoff.invest import Client, Bond, InstrumentIdType

DATETIME_FORMAT = '%d-%m-%Y'

def show_money (money):
    value = money.units + money.nano/10000000000
    return str(value) + " " + money.currency

def show_bond(bond: Bond, coupons = [], separator = '|'):
    sep = separator
    start_date = bond.state_reg_date.strftime(DATETIME_FORMAT)
    end_date = bond.maturity_date.strftime(DATETIME_FORMAT)
    years = bond.maturity_date.year - bond.state_reg_date.year
    last_years = bond.maturity_date.year - date.today().year

    dates = f'{years:2} {sep} {last_years:2} {sep} {start_date} {sep} {end_date}'
    money = f'{show_money(bond.nominal):>12} {sep} {show_money(bond.aci_value):>10}'
    print(f"{bond.name} {sep} {bond.ticker} {sep} {bond.floating_coupon_flag:1} {sep} {dates} {sep} {money} {sep}")
    return 0

def main(args):
    load_dotenv()
    token = os.getenv("TOKEN", "")
    
    with Client(token) as client:
        bonds = client.instruments.bonds()
        for bond in bonds.instruments:
            if 'SU' in bond.ticker and bond.sector == 'government' and bond.floating_coupon_flag is False:
                # coupons = client.instruments.get_bond_coupons(figi=bond.instrument.figi)
                show_bond(bond=bond)
        
        # bond = client.instruments.bond_by(id_type=InstrumentIdType(2), class_code='TQOB', id='SU29008RMFS8')
        # print(bond)
        # coupons = client.instruments.get_bond_coupons(figi=bond.instrument.figi)
        # for coupon in coupons.events:
        #     print(coupon)

    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv))
