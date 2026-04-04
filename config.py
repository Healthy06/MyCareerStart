import os
from dotenv import load_dotenv

load_dotenv()

HH_API_URL = "https://api.hh.ru/vacancies"
HH_API_REGION = 3
HH_API_VACANCIES_PER_PAGE = 5  

BOT_TOKEN = os.getenv("BOT_TOKEN")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")