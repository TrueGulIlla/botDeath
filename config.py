import os
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv("DB_NAME", "users.db")

BOT_TOKEN = os.getenv('BOT_TOKEN')
DB_URL = f"sqlite+aiosqlite:///{DB_NAME}"

if not BOT_TOKEN: 
    raise ValueError('Error no token')
