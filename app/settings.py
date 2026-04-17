from dotenv import dotenv_values
from pathlib import Path
from os import environ

BASE_PATH = Path(__file__).parent.parent
is_docker = environ.get('IS_DOCKER', '0') == '1'

if is_docker:
    DB_HOST = environ.get('DB_HOST')
    DB_PORT = int(environ.get('DB_PORT'))
    DB_NAME = environ.get('DB_NAME')
    DB_USER = environ.get('DB_USER')
    DB_PASSWORD = environ.get('DB_PASSWORD')
    LOG_FILE_PATH = Path(environ.get('LOG_FILE_PATH'))
    LIMIT_LOG_WRITES_PER_HOUR = environ.get('LIMIT_LOG_WRITES_PER_HOUR')
else:
    ENV = dotenv_values(BASE_PATH / '.env')
    DB_HOST = ENV['DB_HOST']
    DB_PORT = int(ENV['DB_PORT'])
    DB_NAME = ENV['DB_NAME']
    DB_USER = ENV['DB_USER']
    DB_PASSWORD = ENV['DB_PASSWORD']
    LOG_FILE_PATH = Path(ENV['LOG_FILE_PATH'])
    LIMIT_LOG_WRITES_PER_HOUR = ENV['LIMIT_LOG_WRITES_PER_HOUR']

if not LOG_FILE_PATH.is_absolute():
    LOG_FILE_PATH = BASE_PATH / LOG_FILE_PATH