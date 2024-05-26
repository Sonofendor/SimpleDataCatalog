from configparser import ConfigParser
from dotenv import load_dotenv
import os

load_dotenv()
CONFIG_PATH = os.getenv('CONFIG_PATH')

app_config = ConfigParser()
app_config.read(CONFIG_PATH)

if os.getenv('BACKEND_DB_CONN'):
    app_config['DATABASE']['BACKEND_DB_CONN'] = os.getenv('BACKEND_DB_CONN')
