from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def create_language_keyboard(language_dict, row_width=3, prefix='') -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()
    buttons: list[InlineKeyboardButton] = []
    for language_name, language_code in language_dict.items():
        callback_data = f'{prefix}_{language_code}'
        buttons.append(InlineKeyboardButton(text=language_name, callback_data=callback_data))
    keyboard.row(*buttons, width=row_width)
    return keyboard.as_markup()
