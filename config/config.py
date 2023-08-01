from environs import Env

env = Env()
env.read_env()

# Bot Credentials
BOT_TOKEN = env.str("BOT_TOKEN")

# Database Credentials
HOST = env.str("HOST")
DBNAME = env.str("DBNAME")
USER = env.str("USER")
PORT = env.str("PORT")
PASSWORD = env.str("PASSWORD")

REG_PAGE_TIME = env.int("REG_PAGE_TIME")
