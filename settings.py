from os import getenv
from dotenv import load_dotenv

load_dotenv()

CHAVE = getenv('CHAVE')

# Banco SQL Server
MS_HOST = getenv('MS_HOST')
MS_PORT = getenv('MS_PORT')
MS_USER = getenv('MS_USER')
MS_PASSWORD = getenv('MS_PASSWORD')
MS_DB = getenv('MS_DB')

MENTOR_URL = getenv('MENTOR_URL')
MENTOR_USER = getenv('MENTOR_USER')
MENTOR_PASSWORD = getenv('MENTOR_PASSWORD')
