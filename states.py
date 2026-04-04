from aiogram.fsm.state import State, StatesGroup


class CareerForm(StatesGroup):
    age = State()
    education = State()
    interests = State()
    subjects = State()
    skills = State()
    work_format = State()
    goal = State()