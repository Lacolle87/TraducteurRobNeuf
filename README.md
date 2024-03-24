wtire it nicely

# Traducteur Rob Neuf

«Neuf» - from French language may mean «nine» or «new» - it's up to you to decide.

## Introduction

Welcome to our multi-language translator bot!

This is not your average translator bot.

To get a translation, simply type in your message.

We support translation between 9 languages and even have an auto-detect feature for convenience.

🇨🇳 Chinese
🇬🇧 English
🇮🇳 Hindi
🇪🇸 Spanish
🇫🇷 French
🇸🇦 Arabic
🇧🇩 Bengali
🇵🇹 Portuguese
🇷🇺 Russian
🌐 Auto Detect

The project employs [aiogram](https://github.com/aiogram/aiogram), [googletrans](https://github.com/ssut/py-googletrans)
and [psycopg](https://github.com/psycopg/psycopg) for its core functionalities.

Users configurations are stored in [PostgreSQL database](https://www.postgresql.org),
with user IDs hashed using SHA256 to ensure they cannot be retrieved again.

## Project structure

```bash
TraducteurRobNeuf
├── config_data
│   └── config.py
│   └── langs.py
├── database
│   └── select_data.py
│   └── users_postgres.py
│   └── users_stats.py
├── handlers
│   └── other_handlers.py
│   └── user_handlers.py
├── keyboards
│   └── keyboards.py
│   └── main_menu.py
├── lexicon
│   └── lexicon.py
├── logger
│   └── logger.py
├── services
│   └── services.py
├── .env
├── .env.example
├── .gitignore
├── main.py
├── README.md
└── requirements.txt
```