MESSAGES: dict[str, str] = {
    '/start': 'Bienvenue à «Traducteur Rob Neuf».'
              '\n\nTo get a translation, simply type in your message.'
              '\n\nYou can choose the language by pressing:\n/change_language\nor use the default settings.'
              '\n\nParamètres définis maintenant:',
    '/help': '\nWelcome to our multi-language translator bot!'
             '\n\nThis is not your average translator bot.'
             '\n\nTo get a translation, simply type in your message.'
             '\n\nWe support translation between 9 languages and even have an auto-detect feature for convenience.'
             '\n\nUse /start to begin a new translation session.'
             '\n\nUse /configs to view selected language configurations.'
             '\n\nUse /change_language to select your preferred source and destination languages from the following '
             'options:'
             '\n\n🇨🇳 Chinese'
             '\n🇬🇧 English'
             '\n🇮🇳 Hindi'
             '\n🇪🇸 Spanish'
             '\n🇫🇷 French'
             '\n🇸🇦 Arabic'
             '\n🇧🇩 Bengali'
             '\n🇵🇹 Portuguese'
             '\n🇷🇺 Russian'
             '\n🌐 Auto Detect'
             '\n\nUse /swap_language to switch languages between source and destination.',
    '/change_language': 'Select desired language for translation:',
    '/configs': 'Paramètres définis maintenant:',
    '/swap_language': 'You cannot set destination language to «auto». \n\nPlease change your language configurations:'
                      '\n/change_language',
    '/get_stats': '403 forbidden'
}

LEXICON_COMMANDS: dict[str, str] = {
    '/start': 'Limbo. Latin: limbus, «edge» or «boundary».',
    '/change_language': 'Select.',
    '/configs': 'Create view.',
    '/help': 'Mayday, mayday. Man overboard again.',
    '/swap_language': 'Switch languages.'
}
