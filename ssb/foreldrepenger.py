#!/usr/bin/env python
# coding: utf-8

"""
Produsere csv fil med data fra database:
    Kilde er data fra oracle database
    Output er csv fil
    Input parameter: periode_type. Verdien er enten M eller A. M produserer 12 måneds csv-filer, og A produserer en års csv-fil.
                     Tilsvarende kommandolinje til å starte produsering er enten python foreldrepenger.py M eller python foreldrepenger.py A.
"""

import os, oracledb, pandas as pd
import sys
from kobling_mot_oracle import oracle_secrets
import datetime

def generate_csv(periode_type: str):
    print('generate_csv starter med periode_type:',periode_type)
    """
    periode_type=M : Produserer 12 måneds csv-filer
    periode_type=A : Produserer en års csv-fil
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

    if periode_type == 'M':
        for maaned in range(1, 13, 1): # Loop fra januar til desember
            # Filnavn skal være f.eks. s350_fp_sp_ssb_2025_m01.csv etter krav fra SSB
            maaned = str(maaned) # Konvertere integer til string for bruk av concatenate senere
            if len(maaned) == 1:
                maaned = '0' + maaned
            print('Produsere måned', maaned, 'csv fil starter ', datetime.datetime.now())

            file_path = "S350_FP_SP_SSB_2025_M" + maaned + ".csv"
            with open(file_path, 'w') as f: # with open metode oppretter en ny fil om det ikke finnes, ellers overskriver eksisterende fil
                # Skilletegn er semikolon
                write_header=True
                query = "select * from vfam_fp_sp_ssb_2025_m where stat_aarmnd = 2025" + maaned
                df = pd.read_sql(query, con=connection)
                df.to_csv(file_path, index=False, sep=';', encoding='utf-8', header=write_header, date_format='%Y%m%d')

            print('Produsere måned', maaned, 'csv fil er fullført ', datetime.datetime.now())
    
    if periode_type == 'A':
        print('Produsere års csv fil starter ', datetime.datetime.now())
        file_path = "S350_FP_SP_SSB_2025_A.csv"
        with open(file_path, 'w') as f: # with open metode oppretter en ny fil om det ikke finnes, ellers overskriver eksisterende fil
            # Skilletegn er semikolon
            write_header=True
            query = "select * from vfam_fp_sp_ssb_2025_a"
            df = pd.read_sql(query, con=connection)
            df.to_csv(file_path, index=False, sep=';', encoding='utf-8', header=write_header, date_format='%Y%m%d')

        print('Produsere års csv fil er fullført ', datetime.datetime.now())

def main():
    if len(sys.argv) > 1:
        periode_type = sys.argv[1].upper()
        print('main starter med periode_type:',periode_type)
        generate_csv(periode_type)
    else:
        print("Oppgi periode_type M eller A. Kode kan være enten", "\033[1m"+"python foreldrepenger.py A"+"\033[0m", "eller", "\033[1m"+"python foreldrepenger.py M"+"\033[0m")

if __name__ == "__main__":
    main()