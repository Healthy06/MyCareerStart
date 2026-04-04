import json
import requests
from config import (
    OPENROUTER_API_KEY,
    OPENROUTER_URL,
    MODEL_NAME,
    HH_API_URL,
    HH_API_REGION,
    HH_API_VACANCIES_PER_PAGE
)


def search_vacancies(keywords):
    params = {
        'text': ' '.join(keywords),
        'area': HH_API_REGION,
        'per_page': HH_API_VACANCIES_PER_PAGE,
        'page': 0,
        'order_by': 'publication_time',
    }

    response = requests.get(HH_API_URL, params=params)
    
    if response.status_code == 200:
        vacancies = response.json()['items']
        return vacancies
    else:
        return None


def build_prompt(profile: dict) -> str:
    return f"""
Ты — карьерный консультант для пользователей 16-22 лет.

ВАЖНО:
- Пиши ТОЛЬКО на русском языке
- НЕ используй английские слова
- НЕ пиши лишний текст
- Отвечай строго в JSON
- НЕ добавляй объяснения вне JSON

Данные пользователя:
Возраст: {profile['age']}
Образование: {profile['education']}
Интересы: {profile['interests']}
Предметы: {profile['subjects']}
Навыки: {profile['skills']}
Формат работы: {profile['work_format']}
Цель: {profile['goal']}

Верни JSON строго такого формата:

{{
  "top_directions": [
    "Название профессии 1",
    "Название профессии 2",
    "Название профессии 3"
  ],
  "summary": "Краткое объяснение почему подходит (2-3 предложения)",
  "strengths": [
    "Сильная сторона 1",
    "Сильная сторона 2",
    "Сильная сторона 3"
  ],
  "skills_to_improve": [
    "Навык 1",
    "Навык 2",
    "Навык 3"
  ],
  "first_steps": [
    "Шаг 1",
    "Шаг 2",
    "Шаг 3"
  ]
}}
""".strip()


def analyze_profile_with_ai(profile: dict) -> dict:
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json",
        "HTTP-Referer": "http://localhost",
        "X-Title": "career-bot"
    }

    payload = {
        "model": MODEL_NAME,
        "messages": [
            {"role": "system", "content": "Ты карьерный AI-консультант. Отвечай только валидным JSON."},
            {"role": "user", "content": build_prompt(profile)}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(
            OPENROUTER_URL,
            headers=headers,
            json=payload,
            timeout=120
        )
        response.raise_for_status()

        data = response.json()
        content = data["choices"][0]["message"]["content"].strip()
        content = content.replace("```json", "").replace("```", "").strip()

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            return {
                "top_directions": ["Не удалось определить", "-", "-"],
                "summary": content,
                "strengths": [],
                "skills_to_improve": [],
                "first_steps": []
            }

    except Exception as e:
        return {
            "top_directions": ["AI временно недоступен", "-", "-"],
            "summary": f"Ошибка API: {e}",
            "strengths": [],
            "skills_to_improve": [],
            "first_steps": [
                "Проверь API ключ",
                "Проверь интернет",
                "Проверь лимиты OpenRouter"
            ]
        }