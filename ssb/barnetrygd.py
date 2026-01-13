#!/usr/bin/env python
# coding: utf-8

"""
Produsere csv fil med data fra database:
    Kilde er data fra oracle database
    Output er csv fil
    Input parameter: if_mottaker. Verdien er enten 0 eller 1. 1 betyr å produsere csv fil for mottaker.
                     if_barn. Verdien er enten 0 eller 1. 1 betyr å produsere csv fil for barn.
"""

import os, oracledb, pandas as pd
import sys
from kobling_mot_oracle import oracle_secrets
import datetime

def generate_csv(if_mottaker: int, if_barn: int):
    print('generate_csv starter med if_mottaker:',if_mottaker, ', if_barn:',if_barn)
    """
    if_mottaker=1 : Produsere csv fil for mottaker
    if_barn=1     : Produsere csv fil for barn
    """
    # Koble opp mot oracle database
    oracle_info = oracle_secrets()
    user = oracle_info['user']
    print('Koble opp mot oracle database med user:', user)
    dsn_tns = oracledb.makedsn(oracle_info['host'], 1521, service_name = oracle_info['service'])
    connection = oracledb.connect(user=user, password=oracle_info['password'], dsn=dsn_tns)
    print('Koblet opp mot oracle database vellykket.')

    import warnings
    warnings.filterwarnings('ignore') # Slå av unødvendig varsling ved bruk av pd.read_sql 

    if if_mottaker == 1:
        print('Produsere csv fil for mottaker starter ', datetime.datetime.now())
        # Tøm filen om det finnes fra før
        file_path = "s350_bt_mottaker_ssb_2025.csv"
        with open(file_path, 'w') as f:
            # Barnetrygd mottaker. Insert alle rader til csv i batch modus.
            # Skilletegn er semikolon
            query = "select * from vfam_bt_mottaker_ssb_2025"
            write_header=True
            for chunk in pd.read_sql(query, con=connection, chunksize=10000):
                chunk.to_csv(os.path.join('s350_bt_mottaker_ssb_2025.csv'), mode='a', index=False, sep=';', encoding='utf-8', header=write_header)
                write_header=False
        print('Produsere csv fil for mottaker er fullført ', datetime.datetime.now())
    
    if if_barn == 1:
        print('Produsere csv fil for barn starter ', datetime.datetime.now())
        # Tøm filen om det finnes fra før
        file_path = "s350_bt_barn_ssb_2025.csv"
        with open(file_path, 'w') as f:
            # Barnetrygd barn. Insert alle rader til csv i batch modus.
            # Skilletegn er semikolon
            query = "select * from vfam_bt_barn_ssb_2025"
            write_header=True
            for chunk in pd.read_sql(query, con=connection, chunksize=10000):
                chunk.to_csv(os.path.join('s350_bt_barn_ssb_2025.csv'), mode='a', index=False, sep=';', encoding='utf-8', header=write_header)
                write_header=False
        print('Produsere csv fil for barn er fullført ', datetime.datetime.now())

def main():
    if len(sys.argv) > 1:
        if_mottaker = int(sys.argv[1])
        if_barn = int(sys.argv[2])
        print('main starter med if_mottaker:',if_mottaker, ', if_barn:',if_barn)
        generate_csv(if_mottaker, if_barn)

if __name__ == "__main__":
    main()