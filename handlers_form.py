from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.context import FSMContext
from ai_service import analyze_profile_with_ai, search_vacancies

from states import CareerForm
from keyboards import (
    start_keyboard,
    education_keyboard,
    work_format_keyboard,
    goal_keyboard
)
from database import save_user_profile
from ai_service import analyze_profile_with_ai

router = Router()


START_TEXT = """
👋 Привет! Я AI-карьерный навигатор.

Помогу тебе:
🎯 понять, какая профессия тебе подходит
📈 прокачать навыки
💼 найти стажировку, подработку или первую работу

Это займет всего пару минут ⏳
Готов начать?
"""


@router.message(F.text == "/start")
async def cmd_start(message: Message):
    await message.answer(START_TEXT, reply_markup=start_keyboard())


@router.callback_query(F.data == "start_form")
async def start_form(callback: CallbackQuery, state: FSMContext):
    await state.set_state(CareerForm.age)
    await callback.message.answer(
        "📅 Сколько тебе лет?\n\nПросто напиши число, например: 18",
        reply_markup=ReplyKeyboardRemove()
    )
    await callback.answer()


@router.message(CareerForm.age)
async def process_age(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗ Пожалуйста, напиши возраст числом. Например: 18")
        return

    age = int(message.text)

    if age < 10 or age > 100:
        await message.answer("❗ Введи корректный возраст.")
        return

    await state.update_data(age=age)
    await state.set_state(CareerForm.education)
    await message.answer(
        "🎓 Где ты сейчас учишься или учился?",
        reply_markup=education_keyboard()
    )


@router.message(CareerForm.education)
async def process_education(message: Message, state: FSMContext):
    await state.update_data(education=message.text)
    await state.set_state(CareerForm.interests)
    await message.answer(
        "💡 Что тебе больше всего нравится?\n\n"
        "Можно выбрать несколько и написать через запятую:\n\n"
        "💻 Технологии / программирование\n"
        "📊 Аналитика / цифры\n"
        "🎨 Дизайн / творчество\n"
        "📢 Общение / люди\n"
        "💼 Бизнес / деньги\n"
        "🎮 Игры / медиа / контент",
        reply_markup=ReplyKeyboardRemove()
    )


@router.message(CareerForm.interests)
async def process_interests(message: Message, state: FSMContext):
    await state.update_data(interests=message.text)
    await state.set_state(CareerForm.subjects)
    await message.answer(
        "📚 Какие предметы тебе нравятся?\n\n"
        "Например:\n"
        "математика, информатика, русский, английский"
    )


@router.message(CareerForm.subjects)
async def process_subjects(message: Message, state: FSMContext):
    await state.update_data(subjects=message.text)
    await state.set_state(CareerForm.skills)
    await message.answer(
        "🛠 Какие у тебя уже есть навыки?\n\n"
        "Например:\n"
        "Python, Excel, монтаж видео, дизайн, общение с людьми\n\n"
        "Если пока нет — напиши: нет"
    )


@router.message(CareerForm.skills)
async def process_skills(message: Message, state: FSMContext):
    await state.update_data(skills=message.text)
    await state.set_state(CareerForm.work_format)
    await message.answer(
        "🏢 Какой формат работы тебе ближе?",
        reply_markup=work_format_keyboard()
    )


@router.message(CareerForm.work_format)
async def process_work_format(message: Message, state: FSMContext):
    await state.update_data(work_format=message.text)
    await state.set_state(CareerForm.goal)
    await message.answer(
        "🎯 Зачем тебе работа сейчас?",
        reply_markup=goal_keyboard()
    )


@router.message(CareerForm.goal)
async def process_goal(message: Message, state: FSMContext):
    await state.update_data(goal=message.text)

    data = await state.get_data()

    await save_user_profile(
        tg_id=message.from_user.id,
        age=data["age"],
        education=data["education"],
        interests=data["interests"],
        subjects=data["subjects"],
        skills=data["skills"],
        work_format=data["work_format"],
        goal=data["goal"]
    )

    await message.answer(
        "🔥 Отлично! Я проанализировал твои ответы...\n\n"
        "🧠 Сейчас подберу для тебя:\n"
        "— подходящие направления\n"
        "— сильные стороны\n"
        "— навыки для прокачки\n"
        "— первые шаги\n\n"
        "⏳ Это займет пару секунд...",
        reply_markup=ReplyKeyboardRemove()
    )

    profile = {
        "age": data["age"],
        "education": data["education"],
        "interests": data["interests"],
        "subjects": data["subjects"],
        "skills": data["skills"],
        "work_format": data["work_format"],
        "goal": data["goal"]
    }

    ai_result = analyze_profile_with_ai(profile)

    text = (
        "✨ *Твой карьерный разбор*\n\n"
        f"🎯 *Подходящие направления:*\n"
        f"1. {ai_result['top_directions'][0] if len(ai_result['top_directions']) > 0 else '-'}\n"
        f"2. {ai_result['top_directions'][1] if len(ai_result['top_directions']) > 1 else '-'}\n"
        f"3. {ai_result['top_directions'][2] if len(ai_result['top_directions']) > 2 else '-'}\n\n"
        f"🧠 *Краткий вывод:*\n{ai_result['summary']}\n\n"
        f"💪 *Сильные стороны:*\n" +
        "\n".join([f"• {item}" for item in ai_result.get("strengths", [])]) +
        "\n\n📈 *Что прокачать:*\n" +
        "\n".join([f"• {item}" for item in ai_result.get("skills_to_improve", [])]) +
        "\n\n🚀 *Первые шаги:*\n" +
        "\n".join([f"• {item}" for item in ai_result.get("first_steps", [])])
    )

    keywords = data["interests"].split(",")  
    vacancies = search_vacancies(keywords)

    if vacancies:
        text += "\n\n📢 *Подходящие вакансии:*\n"
        for idx, vacancy in enumerate(vacancies):
            text += f"{idx + 1}. {vacancy['name']} - {vacancy['area']['name']}\n" \
                    f"Ссылка: [Перейти](https://hh.ru/vacancy/{vacancy['id']})\n"
    else:
        text += "\n\n❗ К сожалению, не удалось найти вакансии."

    await message.answer(text, parse_mode="Markdown")
    await state.clear()