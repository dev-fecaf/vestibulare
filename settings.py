from os import getenv
from dotenv import load_dotenv

load_dotenv(dotenv_path='.env.anglo')

CHAVE = getenv('CHAVE')
VESTIBULARE_URL=getenv('VESTIBULARE_URL')

# Banco SQL Server
MS_HOST = getenv('MS_HOST')
MS_PORT = getenv('MS_PORT')
MS_USER = getenv('MS_USER')
MS_PASSWORD = getenv('MS_PASSWORD')
MS_DB = getenv('MS_DB')

MENTOR_URL = getenv('MENTOR_URL')
MENTOR_USER = getenv('MENTOR_USER')
MENTOR_PASSWORD = getenv('MENTOR_PASSWORD')

MENTOR_TURMA = getenv('MENTOR_TURMA')
MENTOR_RA = getenv('MENTOR_RA')

TEST = getenv('TEST')
