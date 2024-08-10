from aiogram.fsm.state import State, StatesGroup


class MoodForm(StatesGroup):
    mood = State()


class JournalForm(StatesGroup):
    entry = State()


class NavigationForm(StatesGroup):
    current_index = State()


class Forum(StatesGroup):
    name = State()
