#!/usr/bin/env python
# coding: utf-8

"""
Produsere csv fil med data fra database:
    Kilde er data fra oracle database
    Output er csv fil
    Input parameter: Ingen.
                     Kommandolinje til å starte produsering er python kontantstotte.py.
"""

import os, oracledb, pandas as pd
import sys
from kobling_mot_oracle import oracle_secrets
import datetime

def generate_csv():
    print('generate_csv starter:')

    # Koble opp mot oracle database
    oracle_info = oracle_secrets()
    user = oracle_info['user']
    print('Koble opp mot oracle database med user:', user)
    dsn_tns = oracledb.makedsn(oracle_info['host'], 1521, service_name = oracle_info['service'])
    connection = oracledb.connect(user=user, password=oracle_info['password'], dsn=dsn_tns)
    print('Koblet opp mot oracle database vellykket.')

    import warnings
    warnings.filterwarnings('ignore') # Slå av unødvendig varsling ved bruk av pd.read_sql
    
    print('Produsere csv fil starter ', datetime.datetime.now())
    file_path = "S350_KS_MOTTAKER_2025.csv"
    with open(file_path, 'w') as f: # with open metode oppretter en ny fil om det ikke finnes, ellers overskriver eksisterende fil
        # Skilletegn er semikolon
        write_header=True
        query = "select * from vfam_ks_mottaker_2025"
        df = pd.read_sql(query, con=connection)
        df.to_csv(file_path, index=False, sep=';', encoding='utf-8', header=write_header, date_format='%Y%m%d')

    print('Produsere csv fil er fullført ', datetime.datetime.now())

def main():
    print('main starter:')
    generate_csv()

if __name__ == "__main__":
    main()