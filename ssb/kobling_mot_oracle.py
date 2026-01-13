"""
1. Koble opp mot oracle database med konfigurasjon fra GCP Secret Manager
2. .env fil kreves for test på lokal Knast:
    . Spesifisere hvor ['KNADA_TEAM_SECRET']}/versions/latest ligger
    . Variabel user og password er hentet fra .env og er til personlig bruker.
"""

import os, json
from google.cloud import secretmanager

def set_secrets_as_envs():
    # Kommunikasjon mot Google Cloud Secret Manager
    # Hent inn oppsett av miljøvariabler
    from dotenv import load_dotenv
    load_dotenv()

    secrets = secretmanager.SecretManagerServiceClient()
    resource_name = f"{os.environ['KNADA_TEAM_SECRET']}/versions/latest"
    secret = secrets.access_secret_version(name=resource_name)
    secret_str = secret.payload.data.decode('UTF-8')
    secrets = json.loads(secret_str)
    os.environ.update(secrets)

def oracle_secrets():
    set_secrets_as_envs()
    return dict(
    user = os.getenv("PERSONLIG_ORCL_USER"), # Endres til DBT_ORCL_USER når kode kjøres fra Knorten
    password = os.getenv("PERSONLIG_ORCL_PASS"), # Endres til DBT_ORCL_PASS når kode kjøres fra Knorten
    host = os.getenv("DBT_ORCL_HOST"),
    service = os.getenv("DBT_ORCL_SERVICE"),
    encoding = "UTF-8",
    nencoding = "UTF-8"
    )