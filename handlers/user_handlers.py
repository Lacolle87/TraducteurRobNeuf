from aiogram import F, Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, Message, ContentType
from lexicon.lexicon import MESSAGES
from database.users_sqlite import load_users_config, save_users_config
from database.stats_data import save_stats
from services.services import translate, hash_user_id
from keyboards.keyboards import create_language_keyboard
from config_data.langs import bot_lang_from, bot_lang_to, reversed_bot_lang_from, reversed_bot_lang_to

router = Router()
users_config = load_users_config()


def get_hashed_user_id(message: Message) -> str:
    user_id = str(message.from_user.id)
    hashed_user_id = hash_user_id(user_id)
    return hashed_user_id


def get_language_names(hashed_user_id: str) -> tuple[str, str, str, str]:
    src_lang = users_config[hashed_user_id]['src_lang']
    dest_lang = users_config[hashed_user_id]['dest_lang']
    src_name = reversed_bot_lang_from.get(src_lang)
    dest_name = reversed_bot_lang_to.get(dest_lang)
    return src_name, dest_name, src_lang, dest_lang


@router.message(Command(commands='start'))
async def start_message(message: Message):
    user_id = str(message.from_user.id)
    hashed_user_id = hash_user_id(user_id)
    if hashed_user_id not in users_config:
        users_config[hashed_user_id] = {
            'src_lang': 'auto',
            'dest_lang': 'en'
        }
    src_name, dest_name, _, _ = get_language_names(hashed_user_id)
    save_users_config(users_config)
    await message.answer(f'{MESSAGES["/start"]}\n{src_name} ->> {dest_name}')


@router.message(Command(commands='change_language'))
async def change_language(message: Message):
    src_name, dest_name, _, _ = get_language_names(get_hashed_user_id(message))
    await message.answer(MESSAGES['/change_language'])
    await message.answer(f'Source: {src_name}', reply_markup=create_language_keyboard(bot_lang_from, prefix='FROM'))
    await message.answer(f'Destination: {dest_name}', reply_markup=create_language_keyboard(bot_lang_to, prefix='TO'))


@router.message(Command(commands='swap_language'))
async def swap_language(message: Message):
    user_id = str(message.from_user.id)
    hashed_user_id = hash_user_id(user_id)
    src_name, dest_name, src_lang, dest_lang = get_language_names(hashed_user_id)
    if src_lang == 'auto':
        await message.answer(MESSAGES['/swap_language'])
    else:
        users_config[hashed_user_id]['src_lang'] = dest_lang
        users_config[hashed_user_id]['dest_lang'] = src_lang
        save_users_config(users_config)
        await message.answer(f'{MESSAGES["/configs"]}\n{dest_name} ->> {src_name}')


@router.message(Command(commands='help'))
async def help_message(message: Message):
    await message.answer(MESSAGES['/help'])


@router.message(Command(commands='configs'))
async def configs_message(message: Message):
    src_name, dest_name, _, _ = get_language_names(get_hashed_user_id(message))
    await message.answer(f'{MESSAGES["/configs"]}\n{src_name} ->> {dest_name}')


@router.message(F.content_type == ContentType.TEXT)
async def send_translation(message: Message):
    hashed_user_id = get_hashed_user_id(message)
    hashed_user_config = users_config.get(hashed_user_id, {})
    translated_text = translate(message.text,
                                **{lang: hashed_user_config.get(lang) for lang in ['src_lang', 'dest_lang']})
    save_stats(users_config)
    await message.answer(translated_text)


@router.callback_query(F.data.startswith('FROM'))
async def source_language(callback: CallbackQuery):
    language_code = callback.data.split('_')[-1]
    user_id = str(callback.from_user.id)
    hashed_user_id = hash_user_id(user_id)
    users_config[hashed_user_id]['src_lang'] = language_code
    language_name = next((lang for lang, code in bot_lang_from.items() if code == language_code))
    save_users_config(users_config)
    await callback.message.edit_text(f'Source: {language_name}',
                                     reply_markup=create_language_keyboard(bot_lang_from, prefix='FROM'))


@router.callback_query(F.data.startswith('TO'))
async def destination_language(callback: CallbackQuery):
    language_code = callback.data.split('_')[-1]
    user_id = str(callback.from_user.id)
    hashed_user_id = hash_user_id(user_id)
    users_config[hashed_user_id]['dest_lang'] = language_code
    language_name = next((lang for lang, code in bot_lang_from.items() if code == language_code), None)
    save_users_config(users_config)
    await callback.message.edit_text(f'Destination: {language_name}',
                                     reply_markup=create_language_keyboard(bot_lang_to, prefix='TO'))
