#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os, json, oracledb, pandas as pd
from google.cloud import secretmanager
import paramiko
from io import StringIO


# In[ ]:

def set_secrets_as_envs():
    from dotenv import load_dotenv
    load_dotenv()
    secrets = secretmanager.SecretManagerServiceClient()
    resource_name = f"{os.environ['KNADA_TEAM_SECRET']}/versions/latest"
    secret = secrets.access_secret_version(name=resource_name)
    secret_str = secret.payload.data.decode('UTF-8')
    secrets = json.loads(secret_str)
    os.environ.update(secrets)


# In[ ]:


def oracle_secrets():
    set_secrets_as_envs()
    return dict(
    user = os.getenv("DB_SECRET_USER"),
    password = os.getenv("DB_SECRET_PASSWORD"),
    host = os.getenv("DB_ORCL_DSN"),
    service = os.getenv("DB_ORCL_SERVICE"),
    encoding = "UTF-8",
    nencoding = "UTF-8"
    )


# In[ ]:


oracle_info = oracle_secrets()


# In[ ]:


user = oracle_info['user'] + '[DVH_FAM_BT]'
dsn_tns = oracledb.makedsn(oracle_info['host'], 1521, service_name = oracle_info['service'])


# In[ ]:


connection = oracledb.connect(user=user, password=oracle_info['password'], dsn=dsn_tns)


# In[ ]:


# Barnetrygd mottaker Insert alle rader til csv i batch modus
query = "select * from vfam_bt_mottaker_ssb_2025"
write_header=True
for chunk in pd.read_sql(query, con=connection, chunksize=10000):
    chunk.to_csv(os.path.join('s350_bt_mottaker_ssb_2025.csv'), mode='a', index=False, sep=';', encoding='utf-8', header=write_header)
    write_header=False

