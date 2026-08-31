from os import getenv
from discord import Intents
from dotenv import load_dotenv

load_dotenv()

TOKEN = getenv("TOKEN")
INTENTS = Intents.default()

STATUS = getenv("STATUS", "Femboys")
FEMBOYS = int(getenv("FEMBOY_COUNT", 0))
MONTHLY_RESET = bool(getenv("MONTHLY_RESET", False))
RESET_STATUS = False
API = getenv("API", "https://femboyfinder.firestreaker2.dev/api")

REDIS_HOST = getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(getenv("REDIS_PORT", "6379"))
REDIS_DB = int(getenv("REDIS_DB", "0"))
