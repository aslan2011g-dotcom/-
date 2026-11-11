import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBAPP_URL = os.getenv("WEBAPP_URL")  # https://твой-домен/webapp/
