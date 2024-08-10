from aiogram.types import InlineKeyboardButton, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder

from bot_app.services.journal import Journal


class InlineBuilder:

    @staticmethod
    def get_mood_rating():
        inline_kb = InlineKeyboardBuilder()
        for i in range(1, 11):
            inline_kb.add(InlineKeyboardButton(text=str(i), callback_data=f"mood_{i}"))
        inline_kb.adjust(3)
        return inline_kb.as_markup(resize_keyboard=True)

    @staticmethod
    def get_main_menu():
        inline_kb = InlineKeyboardBuilder()
        inline_kb.button(text="Оценить настроение", callback_data='rate_mood')
        inline_kb.button(text="Добавить запись", callback_data='write_entry')
        inline_kb.button(text="Посмотреть записи", callback_data='watch_entries')
        inline_kb.adjust(2)
        return inline_kb.as_markup()

    @staticmethod
    def get_write_kb():
        inline_kb = InlineKeyboardBuilder()
        inline_kb.button(text="Добавить запись", callback_data='write_entry')
        return inline_kb.as_markup()

    @staticmethod
    def get_watch_kb():
        inline_kb = InlineKeyboardBuilder()
        inline_kb.button(text="Посмотреть записи", callback_data='watch_entries')
        return inline_kb.as_markup()

    @staticmethod
    def get_navigation(current_index, user_id):
        inline_kb = InlineKeyboardBuilder()

        # Check for the first entry
        if current_index > 0:
            inline_kb.add(
                InlineKeyboardButton(text="Предыдущая", callback_data="prev_entry")
            )

        # Check for the last entry
        if Journal.get_entry_by_index(user_id, current_index + 1):
            inline_kb.add(
                InlineKeyboardButton(text="Следующая", callback_data="next_entry")
            )

        inline_kb.adjust(2)
        return inline_kb.as_markup()

    @staticmethod
    def get_write_choice():
        inline_kb = InlineKeyboardBuilder()
        inline_kb.button(text="Добавить запись", callback_data='write_entry')
        inline_kb.button(text="Нет, спасибо", callback_data='cancelling')
        return inline_kb.as_markup()


class ReplyBuilder:
    @staticmethod
    def get_mood_keyboard():
        rk_builder = ReplyKeyboardBuilder()
        for i in range(1, 11):
            rk_builder.add(KeyboardButton(text=str(i)))
        rk_builder.adjust(4)
        return rk_builder.as_markup(resize_keyboard=True)
