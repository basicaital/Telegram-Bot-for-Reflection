from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from .states import MoodForm, JournalForm, NavigationForm
from bot_app.services.mood_tracker import MoodTracker
from bot_app.services.motivation import get_motivation
from bot_app.services.journal import Journal
from .keyboards import InlineBuilder

start_router = Router()


def main_keyboard():
    return InlineBuilder.get_main_menu()


@start_router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    welcome_message = (
        "<b>Привет! 🌟 Так здорово, что вы здесь! Я ваш личный помощник и друг, готовый поддержать вас в любой "
        "ситуации.</b>\n\n "
        "Вот, что мы можем сделать вместе:\n"
        "🔹 Оценить ваше настроение и подобрать для вас поддержку\n"
        "🔹 Записать ваши мысли в личный дневник, чтобы всегда помнить важные моменты\n"
        "🔹 Просмотреть все ваши записи и вдохновиться их содержимым\n\n"
        "Давайте сделаем этот день немного ярче и уютнее! Просто выберите нужное действие из меню ниже, "
        "и я с радостью помогу вам. 😊💫 "
    )
    await message.answer(welcome_message, reply_markup=main_keyboard())
    await state.clear()


@start_router.callback_query(F.data == 'rate_mood')
async def rate_mood(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer('Привет! Какое у вас настроения сегодня по шкале от 1 до 10?',
                               reply_markup=InlineBuilder.get_mood_rating())
    await state.set_state(MoodForm.mood)


@start_router.callback_query(MoodForm.mood, F.data.startswith("mood_"))
async def mood_handler(query: CallbackQuery, state: FSMContext):
    try:
        await query.message.delete()
        mood = int(query.data.split("_")[1])
        if mood < 1 or mood > 10:
            raise ValueError('Mood out of range')
        MoodTracker.save_mood(query.from_user.id, mood)
        advice = get_motivation(mood)
        await query.message.answer(advice)
        await state.clear()
        await query.message.answer('Хотите ли записать заметку?', reply_markup=InlineBuilder.get_write_choice())
    except ValueError:
        await query.message.answer('Пожалуйста, введите число от 1 до 10.')


@start_router.callback_query(F.data == 'write_entry')
async def add_journal_entry(query: CallbackQuery, state: FSMContext):
    await query.message.delete()
    await query.message.answer('Введите вашу запись для дневника:')
    await state.set_state(JournalForm.entry)


@start_router.message(JournalForm.entry)
async def save_journal_entry(message: Message, state: FSMContext):
    entry = message.text
    Journal.add_entry(message.from_user.id, entry)
    await message.answer('Ваша запись сохранена.', reply_markup=InlineBuilder.get_watch_kb())
    await state.clear()


@start_router.message(Command('add_entry'))
async def add_entry(message: Message):
    await message.answer("Рефлексируйте", reply_markup=InlineBuilder.get_write_kb())


@start_router.callback_query(F.data == 'watch_entries')
async def inline_view_entries(callback_query: CallbackQuery, state: FSMContext):
    entries = Journal.get_entries(callback_query.from_user.id)
    if entries == 'У вас нет записей':
        await callback_query.message.edit_text(entries)
        return
    first_entry = Journal.get_entry_by_index(callback_query.from_user.id, 0)
    if first_entry:
        entry_text = f"{first_entry['timestamp']}: \n{first_entry['entry']}"
        await callback_query.message.edit_text(entry_text,
                                               reply_markup=InlineBuilder.get_navigation(0,
                                                                                         callback_query.from_user.id))
        await state.update_data(current_index=0)
        await state.set_state(NavigationForm.current_index)


@start_router.callback_query(F.data.in_({'prev_entry', 'next_entry'}))
async def navigation_entry(query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    current_index = data.get('current_index', 0)

    if query.data == 'prev_entry':
        current_index = max(0, current_index - 1)
    elif query.data == 'next_entry':
        current_index += 1

    entry = Journal.get_entry_by_index(query.from_user.id, current_index)
    if entry:
        entry_text = f"{entry['timestamp']}: \n{entry['entry']}"
        await query.message.edit_text(entry_text,
                                      reply_markup=InlineBuilder.get_navigation(current_index, query.from_user.id))
        await state.update_data(current_index=current_index)
    else:
        await query.message.edit_text('Больше нет записей',
                                      reply_markup=InlineBuilder.get_navigation(current_index, query.from_user.id))


@start_router.callback_query(F.data == "cancelling")
async def cancel_choice(query: CallbackQuery):
    await query.message.edit_text("Хорошего дня!")





