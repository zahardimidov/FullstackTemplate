from os import getenv
from dotenv import load_dotenv
from pathlib import Path
import pytz

BASE_DIR = Path(__file__).parent.resolve()

ENV_FILE = BASE_DIR.joinpath(getenv('ENV')) if getenv('ENV') else BASE_DIR.joinpath('.localenv')

load_dotenv(ENV_FILE)

DEBUG = bool(getenv('DEBUG', 1))
PORT = getenv('PORT', 8080)
HOST = getenv('HOST', f'http://0.0.0.0:{PORT}')

ENGINE = getenv('ENGINE', 'sqlite+aiosqlite:///./database/database.db')

REDIS_HOST = getenv('REDIS_HOST', "localhost")
REDIS_PORT = getenv('REDIS_HOST', 6379)

TIMEZONE = pytz.timezone(getenv('TIMEZONE', 'Europe/Moscow'))

'''
ENV=.localenv docker compose up --build --scale backend=1
'''