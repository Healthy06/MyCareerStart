import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL_NAME = "deepseek/deepseek-chat"

HH_API_URL = "https://api.hh.ru/vacancies"
HH_API_REGION = 3
HH_API_VACANCIES_PER_PAGE = 5

DB_PATH = os.getenv("DB_PATH", "career_bot.db")