bot_lang_from = {
    '🇨🇳 Chinese': 'zh-cn',
    '🇬🇧 English': 'en',
    '🇮🇳 Hindi': 'hi',
    '🇪🇸 Spanish': 'es',
    '🇫🇷 French': 'fr',
    '🇸🇦 Arabic': 'ar',
    '🇧🇩 Bengali': 'bn',
    '🇵🇹 Portuguese': 'pt',
    '🇷🇺 Russian': 'ru',
    '🌐 Auto Detect': 'auto'
}

bot_lang_to = {
    '🇨🇳 Chinese': 'zh-cn',
    '🇬🇧 English': 'en',
    '🇮🇳 Hindi': 'hi',
    '🇪🇸 Spanish': 'es',
    '🇫🇷 French': 'fr',
    '🇸🇦 Arabic': 'ar',
    '🇧🇩 Bengali': 'bn',
    '🇵🇹 Portuguese': 'pt',
    '🇷🇺 Russian': 'ru'
}


def get_language_name(lang_code, lang_dict):
    return next((lang for lang, code in lang_dict.items() if code == lang_code), None)


def process_language_names(users_config, user_id, bot_lang_from, bot_lang_to):
    src_name = get_language_name(users_config[user_id]['src_lang'], bot_lang_from)
    dest_name = get_language_name(users_config[user_id]['dest_lang'], bot_lang_to)
    return src_name, dest_name
