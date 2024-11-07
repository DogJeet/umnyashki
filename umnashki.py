# ⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽
# ⎸           ⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽⎽           ⎹
# ⎸           ⎸           ⎹           ⎹
# ⎸           ⎸           ⎹           ⎹
# ⎸           ⎸           ⎹           ⎹
# ⎸           ⎸    olr    ⎹           ⎹
# ⎸           ⎸           ⎹           ⎹
# ⎸           ⎸           ⎹           ⎹
# ⎸           ⎸           ⎹           ⎹
# ⎸           ⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺           ⎹
# ⎸       ver 1.08 p.1 20.08.24       ⎹
# ⎸           satrt 17.08.24          ⎹
# ⎸              by olr               ⎹
# ⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺⎺
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, PhotoSize
import sqlite3
import secrets
import string
from telegram.ext import Updater, CommandHandler, CallbackContext, CallbackQueryHandler, MessageHandler, Filters
import sqlite3
import os
from telegram import InputMediaPhoto

ADMIN_USERNAMES = ['oligarh228', 'MusoraNetM', 'umanna_kam']

CHAT_ID = "-1002172582253"

DB_PATH = "chat_links.db"
def get_chat_link(update, context):
    # Создаем ссылку на чат для текущего пользователя с ограничением 1 пользователь
    chat_link = context.bot.create_chat_invite_link(CHAT_ID, member_limit=1)

conn = sqlite3.connect(DB_PATH)
c = conn.cursor()
c.execute("""CREATE TABLE IF NOT EXISTS chat_links
        (user_id INTEGER PRIMARY KEY, invite_link TEXT)""")
conn.commit()
conn.close()

def get_chat_link(update, context):
    user_id = update.effective_user.id

    # Проверяем, есть ли ссылка для этого пользователя в базе данных
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT invite_link FROM chat_links WHERE user_id = ?", (user_id,))
    result = c.fetchone()

    if result:
        # Если ссылка есть, отправляем ее пользователю
        update.message.reply_text(f"Ссылка на чат: {result[0]}")
    else:
        # Если ссылки нет, создаем новую и сохраняем ее в базе данных
        chat_link = context.bot.create_chat_invite_link(CHAT_ID, member_limit=10)
        c.execute("INSERT INTO chat_links (user_id, invite_link) VALUES (?, ?)", (user_id, chat_link.invite_link))
        conn.commit()
        update.message.reply_text(f"Ссылка на чат: {chat_link.invite_link}")

    conn.close()

# Функция для создания соединения с базой данных
def get_db_connection():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    return conn, c

conn = sqlite3.connect('photos.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS photos
             (user_id INTEGER, file_id TEXT, file_name TEXT)''')
conn.commit()

# Создание таблицы пользователей
conn, c = get_db_connection()
try:
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, chat_id INTEGER UNIQUE)''')
    conn.commit()
except sqlite3.Error as e:
    print(f"Ошибка при создании таблицы: {e}")
finally:
    conn.close()

# Функция для получения списка всех пользователей из базы данных
def get_all_users():
    conn, c = get_db_connection()
    try:
        c.execute("SELECT chat_id FROM users")
        return [row[0] for row in c.fetchall()]
    except sqlite3.Error as e:
        print(f"Ошибка при получении пользователей: {e}")
        return []
    finally:
        conn.close()

# Функция для создания соединения с базой данных
def get_db_connection():
    conn = sqlite3.connect('users.db')
    c = conn.cursor()
    return conn, c


# Создание таблицы пользователей
conn, c = get_db_connection()
try:
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY, chat_id INTEGER UNIQUE)''')
    conn.commit()
except sqlite3.Error as e:
    print(f"Ошибка при создании таблицы: {e}")
finally:
    conn.close()

def start(update: Update, context: CallbackContext):
    with open('jpg/1.jpg', 'rb') as f:
        photo = f.read()
    add_user(update.effective_chat.id)
    user = update.effective_user
    keyboard = [
        [InlineKeyboardButton("Привет 👋", callback_data="next")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    username = update.effective_user.username
    first_name = update.effective_user.first_name
    last_name = update.effective_user.last_name
    
    connection, cursor = get_connection_and_cursor()
    if connection and cursor:
        insert_user(cursor, connection, username, first_name, last_name)
        print("Added!")
        connection.close()
    else:
        print("Oshibka")

    context.bot.send_photo(
        chat_id=update.effective_chat.id,
        photo=photo,
        caption=f"{user.first_name}, привет! 👋 Я Ева – помощница детской развивающей студии «УМняшки» для детей от 2 лет!\n"
               "Хотите узнать расписание занятий, описание и цены в 'УМняшках' или записаться к нам? 📚\n"
               "Просто следуйте инструкциям, и я сразу же пришлю вам всю нужную информацию! 📝\n"
               "Не упустите возможность записаться на интересные занятия для вашего ребенка! 🧸",
        reply_markup=reply_markup
    )

# Добавляем пользователя в базу данных
def add_user(chat_id):
    conn, c = get_db_connection()
    try:
        print(f"Trying to add user with chat_id {chat_id}")
        c.execute("INSERT INTO users (chat_id) VALUES (?)", (chat_id,))
        conn.commit()
        print(f"User with chat_id {chat_id} added to the database")
    except sqlite3.IntegrityError:
        print(f"User with chat_id {chat_id} already exists in the database")
    except sqlite3.Error as e:
        print(f"Error when adding user: {e}")
    finally:
        conn.close()

def next_message(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    message = f"Чтобы продолжить, нажмите любую кнопку ✨"
    keyboard = [[InlineKeyboardButton("Получить промокод 🎁", callback_data="promo")],
                [InlineKeyboardButton("Записаться на занятия 📝", callback_data="call")],
                [InlineKeyboardButton("Вступить в чат 💬", callback_data="chat")],
                [InlineKeyboardButton("Услуги 📋", callback_data="uslugi")],
                [InlineKeyboardButton("О нас 🔍", callback_data="onas")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        reply_markup=reply_markup
    )

def handle_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    query.answer()

    if query.data == "call":
        message = "Нажмите на кнопку с более удобным для вас способом связи с нами. 📞"
        keyboard = [[InlineKeyboardButton("Вконтакте 👥", url='https://vk.com/logoped.kamensk')],
                    [InlineKeyboardButton("WhatsApp 💬", url='https://wa.me/79604626477')],
                    [InlineKeyboardButton("Telegram 🤖", url='https://t.me/umanna_kam')],
                    [InlineKeyboardButton("Позвонить ☎️", callback_data='phone')],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)

        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=reply_markup
        )
    elif query.data == "phone":
        message = "Номер для связи: +7 (960) 462-64-77 📞"
        keyboard = [[InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "promo":
        chat_id = update.effective_chat.id
        username = update.effective_user.username
        first_name = update.effective_user.first_name
        last_name = update.effective_user.last_name
        promo_code = generate_promo_code(chat_id, username, first_name, last_name)
        keyboard = [[InlineKeyboardButton("Отправить промокод 📩", callback_data="chat")],
                [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=chat_id,
            text=f"🎉 Вот ваш уникальный промокод: '{promo_code}' 🎉\n\nНажмите на кнопку ниже, чтобы отправить этот промокод в чат 💬",
            reply_markup=reply_markup
        )

    elif query.data == "chat":
        user_id = query.from_user.id

        # Проверяем, есть ли ссылка для этого пользователя в базе данных
        conn = sqlite3.connect(DB_PATH)
        keyboard = [[InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        c = conn.cursor()
        c.execute("SELECT invite_link FROM chat_links WHERE user_id = ?", (user_id,))
        result = c.fetchone()

        if result:
            # Если ссылка есть, отправляем ее пользователю
            chat_id = update.effective_chat.id
            context.bot.send_message(chat_id=chat_id, text=f"Ссылка на чат: {result[0]}", reply_markup=reply_markup)
        else:
            # Если ссылки нет, создаем новую и сохраняем ее в базе данных
            chat_id = update.effective_chat.id
            chat_link = context.bot.create_chat_invite_link(CHAT_ID, member_limit=10)
            c.execute("INSERT INTO chat_links (user_id, invite_link) VALUES (?, ?)", (user_id, chat_link.invite_link))
            conn.commit()
            context.bot.send_message(chat_id=chat_id, text=f"Ссылка на чат: {chat_link.invite_link}", reply_markup=reply_markup)

        conn.close()

    elif query.data == "uslugi":
        message = "▶️Выберите интересующее направление☟"
        keyboard = [[InlineKeyboardButton("Индивидуальные коррекционные занятия 👨‍🏫", callback_data="logopeddefect")],
                    [InlineKeyboardButton("Груповые развивающие занятия 👨‍👩‍👧‍👦", callback_data="groop")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    elif query.data == "logopeddefect":
        message = "▶️Выберите интересующее направление☟"
        keyboard = [[InlineKeyboardButton("Логопед 👨‍⚕️", callback_data="logoped")],
                    [InlineKeyboardButton("Дефектолог 👩‍⚕️", callback_data="defectolog")],
                    [InlineKeyboardButton("«Запуск» речи 🗣️", callback_data="zapusk")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=reply_markup
        )

    elif query.data == "logoped":
        with open('jpg/2.jpg', 'rb') as f1:
            photo1 = f1.read()
        keyboard = [[InlineKeyboardButton("Записаться 📝", callback_data="call")],
                    [InlineKeyboardButton("Вернуться назад 🔙", callback_data="uslugi")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        message = """➡️Логопед необходим ребёнку, если ребёнок не выговаривает звуки или имеет невнятную речь.
Наши логопеды работают на результат, чтобы ребёнок как можно быстрее заговорил красиво
➡️Ребёнку будет интересно заниматься, потому что занятия проходят в игровой форме.
В результате ребёнок будет красиво говорить, и это поможет ему писать без ошибок по русскому языку
➡️Занятие по коррекции звукопроизношения длится стандартно 40 минут, ребёнок занимается 2-3 раза в неделю
💰Стоимость 1 занятия – 700р (абонементная система оплаты – за месяц вперед по количеству занятий)"""
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo = photo1,
            caption=message,
            reply_markup=reply_markup
        )

    elif query.data == "defectolog":
        with open('jpg/3.jpg', 'rb') as f1:
            photo1 = f1.read()
        keyboard = [[InlineKeyboardButton("Записаться 📝", callback_data="call")],
                    [InlineKeyboardButton("Вернуться назад 🔙", callback_data="uslugi")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        message = """👩‍🏫Дефектолог - это специалист, который помогает «дотянуться до условной нормы развития» детям, испытывающим определенные отставания в развитии:
    🔹Задержка речи или ее отсутствие 🗣️
    🔹Расстройства аутистического спектра (РАС) 🧠
    🔹Задержка психического развития (ЗПР) 🧠
    🔹Двигательные расстройства (ДЦП) 🤸‍♀️
Занятия проводит квалифицированный специалист со стажем более 3-х лет. 👨‍🏫
❗️Высокое качество предоставляемых услуг достигается за счет комплексного подхода и применения современных методик для ускорения процесса устранения нарушений. 🔍
➡️Коррекционное занятие длится стандартно 40 минут, ребёнок занимается 2-3 раза в неделю. ⏰
💰Стоимость 1 занятия – 700р (абонементная система оплаты – за месяц вперед по количеству занятий)"""
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo = photo1,
            caption=message,
            reply_markup=reply_markup
        )


    elif query.data == "zapusk":
        with open('jpg/4.jpg', 'rb') as f1:
            photo1 = f1.read()
        keyboard = [[InlineKeyboardButton("Записаться 📝", callback_data="call")],
                    [InlineKeyboardButton("Вернуться назад 🔙", callback_data="uslugi")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=[InputMediaPhoto(photo1)],
        )
        message = """Разговорим каждого молчуна! 🗣️
    🔹Стимуляция речи 🗣️
    🔹Развитие коммуникации 💬
    🔹Формирование слухового восприятия 👂
    🔹Развитие общего и артикуляционного праксиса 👅
    🔹Развитие внимания, памяти, мышления 🧠
▶️На занятиях по запуску и развитию речи ваш ребёнок:
    👉🏻Улучшит понимание обращенной речи; 👂
    👉🏻Научится правильному речевому дыханию; 🤐
    👉🏻Научится произносить отдельные звуки, слоги и слова; 🔤
    👉🏻Научится излагать свои мысли с помощью фразы; 💬
    👉🏻Разовьёт мелкую и крупную моторику; 🙌🦵
    👉🏻Разовьет мышление, внимание, любознательность. 🧠
⏩Программа составлена таким образом, что знания даются ребенку в системе, не урывками. Для каждого ребенка ведется индивидуальный речевой альбом, благодаря которому ребенок закрепляет дома знания, полученные на занятии. 📚
⏩На занятиях используются разные интересные для детей пособия, игры и игрушки, музыкальное сопровождение. Такой подход отлично развивает познавательный интерес детей, помогает быстрее преодолеть проблему отсутствия речи и заговорить. 🎮🎶
➡️Коррекционное занятие длится стандартно 40 минут, ребёнок занимается 2-3 раза в неделю.
💰Стоимость 1 занятия – 700р (абонементная система оплаты – за месяц вперед по количеству занятий)"""
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=reply_markup
        )

    elif query.data == "groop":
        message = "▶️ Выберите подходящую подборку ☟"
        keyboard = [[InlineKeyboardButton("«Раннее развитие» 2-3 года 👶", callback_data="ranrazv")],
                    [InlineKeyboardButton("«Почемучки» 3-4 года 🧒", callback_data="pochemu")],
                    [InlineKeyboardButton("«Развивашки» 4-5 лет 👦", callback_data="razvivashki")],
                    [InlineKeyboardButton("«Подготовишки» 5-8 лет 👨‍🎓", callback_data="podgotovishki")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "ranrazv":
        message = "▶️Выберите подходящую подборку для раннего развития вашего ребенка☟ 👶"
        keyboard = [[InlineKeyboardButton("Мама и малыш 👩‍👦", callback_data="mama")],
                    [InlineKeyboardButton("Логоритмика 🎵", callback_data="logoritmika")],
                    [InlineKeyboardButton("Сказочные истории 🏰", callback_data="story")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "mama":
        with open('jpg/5.jpg', 'rb') as f1:
            photo1 = f1.read()
        keyboard = [[InlineKeyboardButton("Записаться 📝", callback_data="call")],
                    [InlineKeyboardButton("Вернуться назад 🔙", callback_data="uslugi")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=[InputMediaPhoto(photo1)],
        )
        reply_markup = InlineKeyboardMarkup(keyboard)
        message ="""👉 Занятия по всестороннему раннему развитию малыша, где ребёнок будет не только развивать речь, но и развиваться интеллектуально, сенсорно, моторно, творчески, физически и эмоционально. 🧠🤸‍♂️🎨\n\n"
👉 Одно занятие включает от 5 до 7 разных видов деятельности:
    - Участие в разыгрываемой сказке и героями; 🎭
    - Сюжетно-ролевые игры; 🤹‍♀️
    - Лепка, аппликация; 🧶
    - Рисование, развитие мелкой моторики руки; ✏️
    - Сортировки по цвету, форме, размеру; 🔍
    - Дорожка здоровья; 🚶‍♀️
    - Музыкальные паузы; 🎵
    - Подвижные игры; 🏃‍♂️
    - Конструирование; 🧱
    - Сенсорные игры. 🧠

На занятиях Мама и малыш ваш ребёнок:
    ➡️ Улучшит понимание обращенной речи; 👂
    ➡️ Научится правильному речевому дыханию; 🗣️
    ➡️ Научится произносить отдельные звуки, слоги и слова; 🔤
    ➡️ Научится излагать свои мысли с помощью фразы; 💬
    ➡️ Разовьёт мелкую и крупную моторику; 🤲🦵
    ➡️ Разовьет мышление, внимание, любознательность. 🧠

*А самое главное, у ребенка будет развиваться познавательный интерес, что является основой любого развития!* 🔍

⏩ Программа составлена таким образом, что знания даются ребенку в системе, не урывками. Для каждого ребенка ведется индивидуальный речевой альбом, благодаря которому ребенок закрепляет дома знания, полученные на занятии. 📚
⏩ На занятиях используются разные интересные для детей пособия, игры и игрушки, музыкальное сопровождение. Такой подход отлично развивает познавательный интерес детей, помогает быстрее преодолеть проблему отсутствия речи и заговорить. 🎮🎶

➡️ Занятия проходят в мини-группах до 6 человек 2 раза в неделю по 40 минут.
💰 Стоимость 1 занятия – 400р (абонементная система оплаты – за месяц вперед по количеству занятий)"""
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=reply_markup
        )

        
    elif query.data == "logoritmika":
        with open('jpg/6.jpg', 'rb') as f1:
            photo1 = f1.read()
        keyboard = [[InlineKeyboardButton("Записаться 📝", callback_data="call")],
                    [InlineKeyboardButton("Вернуться назад 🔙", callback_data="uslugi")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=[InputMediaPhoto(photo1)],
        )
        message = """Логоритмика для детей – это игровой метод работы с малышами, при котором используются музыкальные, двигательные и словесные элементы.
            
Регулярные занятия логопедической ритмикой:
    🔸 Способствуют нормализации речи ребенка вне зависимости от вида речевого нарушения;
    🔸 Уравновешивают нервно-психические процессы;
    🔸 Снижают агрессивные проявления поведения в быту;
    🔸 Формируют положительный эмоциональный настрой;
     🔸 Помогают детям адаптироваться к условиям внешней среды.

Логоритмика в первую очередь полезна детям:
    🔹 С заиканием или с наследственной предрасположенностью к нему;
    🔹 С чересчур быстрой/медленной или прерывистой речью;
    🔹 С недостаточно развитой моторикой и координацией движений;
    🔹 С дизартрией, задержками развития речи, нарушениями произношения отдельных звуков;
    🔹 Часто болеющим и ослабленным;\n"
    🔹 Находящимся в периоде интенсивного формирования речи (в среднем это возраст от 2,5 до 4 лет).

👥 Занятия проходят в мини-группах до 6 человек 2 раза в неделю по 40 минут.
💰 Стоимость 1 занятия – 400р (абонементная система оплаты – за месяц вперед по количеству занятий)"""
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=reply_markup
        )

    elif query.data == "story":
        with open('jpg/10.jpg', 'rb') as f1:
            photo = f1.read()
        context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=[InputMediaPhoto(photo)],
        )
        message = """Приглашаем ваших малышей на незабываемые приключения в мир русских народных сказок! 🌟
Вашего ребенка ждут увлекательные развивающие занятия, полные ярких эмоций и новых открытий! 🎨

Погрузившись в волшебный мир сказочных героев, ваши дети научатся:
    • Развивать воображение, фантазию и творческие способности 💭
    • Познавать окружающий мир через образы и сюжеты народного творчества 🌍
    • Укреплять нравственные ценности и представления о добре и зле ⚖️

На наших занятиях малыши не просто слушают сказки - они становятся их активными участниками и выполняют разные задания:
    - Дидактические игры на закрепление знаний о персонажах, событиях, предметах из сказки. 🎲
    - Творческие задания: рисование, лепка, аппликация по мотивам сказки. 🎨
    - Двигательные игры и упражнения, отражающие образы героев. 🏃‍♀️

Занятия проводятся в уютной и безопасной обстановке под чутким руководством опытных педагогов. 👩‍🏫
Приглашаем вас и ваших малышей окунуться в удивительный мир русских сказок! 🏰 Записывайтесь прямо сейчас и подарите своим детям незабываемые моменты радости и познания

👥 Занятия проходят в мини-группах до 6 человек 1 раз в неделю по 40 минут.
💰 Стоимость 1 занятия – 400р (абонементная система оплаты – за месяц вперед по количеству занятий)"""
        keyboard = [[InlineKeyboardButton("Записаться 📝", callback_data="call")],
                    [InlineKeyboardButton("Вернуться назад 🔙", callback_data="uslugi")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=reply_markup
        )

    elif query.data == "pochemu":
        message = "▶️ Выберите подходящую подборку ☟"
        keyboard = [[InlineKeyboardButton("🧠 Развивашки 3-4", callback_data="razv1")],
                    [InlineKeyboardButton("📚 Сказочные истории", callback_data="story")],
                    [InlineKeyboardButton("🔙 Вернуться назад", callback_data="uslugi")],
                    [InlineKeyboardButton("🏠 Вернуться в меню", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=reply_markup
        )


    elif query.data == "razv1":
        with open('jpg/7.jpg', 'rb') as f1:
            photo1 = f1.read()
        keyboard = [[InlineKeyboardButton("Записаться 📝", callback_data="call")],
                    [InlineKeyboardButton("Вернуться назад 🔙", callback_data="uslugi")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = """✨Успешное развитие ребенка лежит на 4 китах:
    🔹память
    🔹внимание
    🔹воображение
    🔹мышление

Когда у ребенка развиты эти навыки:
    ✅он легко осваивает чтение, письмо, математику, когда его мозг будет готов к этому.
    ✅быстрее и больше запоминает, хорошо справляется с пересказом.
    ✅с легкостью переключается между задачами.
    ✅развивается гармонично, не опережая важнейшие этапы развития.

❗️Ваш ребенок учится учиться легко!
Это действительно то, что помогает ребенку в школе и в дальнейшем обучении, делает его не просто \"успевающим\", а \"успешным\"!

👥Занятия проходят в мини-группах до 6 человек 2 раза в неделю по 55 минут.
💰Стоимость 1 занятия – 400р (абонементная система оплаты – за месяц вперед по количеству занятий)"""
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo = photo1,
            caption=message,
            reply_markup=reply_markup
        )

    elif query.data == "razvivashki":
        with open('jpg/8.jpg', 'rb') as f1:
            photo1 = f1.read()
        keyboard = [[InlineKeyboardButton("Записаться 📝", callback_data="call")],
                    [InlineKeyboardButton("Вернуться назад 🔙", callback_data="uslugi")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = """
На комплексных занятиях мы, играя,
    🔊 знакомимся со звуками и буквами,
    🔢 изучаем математику,
    🗣️ развиваем речь,
    👥 учимся общаться,
    💃 танцуем,
    🎶 занимаемся логоритмикой,
    🧠 развиваем логику,
    🌍 знакомимся с окружающим миром и пространством,
    🎨 развиваем творческие способности,
    ✏️ готовим руку к письму.

💡 И это всё не просто "развивашки", а уже, непосредственно ПОДГОТОВКА К ШКОЛЕ, конечно же соответствующая возрасту. Поэтому занятия проходят в игровой форме.

📚 У нас нет задачи научить читать детей на этом курсе, т.к. их мозг еще не созрел для такого сложного навыка, но, мы начинаем их знакомить с буквами и даже со слияниями букв, находить звуки в слове, развиваем связную речь.

⏰ Занятия проходят в мини-группах до 6 человек 2 раза в неделю по 55 минут.
💰 Стоимость 1 занятия – 400р (абонементная система оплаты – за месяц вперед по количеству занятий)
        """
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo = photo1,
            caption=message,
            reply_markup=reply_markup
        )


    elif query.data == "podgotovishki":
        message = "▶️Выберите подходящую подборку☟"
        keyboard = [[InlineKeyboardButton("Читай-ка 📚", callback_data="read")],
                    [InlineKeyboardButton("Подготовка к школе 🏫", callback_data="school")],
                    [InlineKeyboardButton("Вернуться назад 🔙", callback_data="uslugi")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    elif query.data == "read":
        with open('jpg/9.jpg', 'rb') as f1:
            photo1 = f1.read()
        keyboard = [[InlineKeyboardButton("Записаться 📝", callback_data="call")],
                    [InlineKeyboardButton("Вернуться назад 🔙", callback_data="uslugi")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=[InputMediaPhoto(photo1)],
        )
        message = """
🔖 Курс игрового обучения чтению «Читай-ка» помогает ребенку сформировать навык слитного чтения слогов и слов, чтения предложений и текстов с пониманием прочитанного.

📚 Занятия проходят в движении, а не за столом. Это делает процесс изучения букв и их слияний интересным и увлекательным.

Ребенок научится:
- 🤓 читать целыми словами и небольшими предложениями;
- 🔊 различать звуки в слове;
- 📚 обогащать словарный запас;
- 🧠 развивать внимание, память, мышление, речь.

👩‍🏫 Педагог заботится о том, чтобы у ребенка сформировался интерес к чтению, а также воспитывает аккуратность, коммуникабельность, любознательность и познавательную активность.

⏰ Занятия проходят в мини-группах до 6 человек 2 раза в неделю по 55 минут.

💰 Стоимость 1 занятия – 400р (абонементная система оплаты – за месяц вперед по количеству занятий)"""

        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=reply_markup
        )

    elif query.data == "school":
        with open('jpg/11.jpg', 'rb') as f1:
            photo1 = f1.read()
        keyboard = [[InlineKeyboardButton("Записаться 📝", callback_data="call")],
                    [InlineKeyboardButton("Вернуться назад 🔙", callback_data="uslugi")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=[InputMediaPhoto(photo1)],
        )
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = """
🏫 Комплексная подготовка к школе включает в себя занятия по грамоте и математике. В программе есть всё необходимое, что позволит ребенку с легкостью поступить в первый класс, адаптироваться и чувствовать себя преуспевающим среди сверстников.

📚 Чему научит курс?

🔢 МАТЕМАТИКА:
    ✨ Формирование математических представлений о числах и цифрах
    ✨ Овладение вычислительными навыками
    ✨ Решение простых задач
    ✨ Закрепление знаний о геометрических фигурах
    ✨ Изучение состава чисел

🔠 ГРАМОТА, ЧТЕНИЕ:
    ✨ Обучение чтению
    ✨ Обогащение словарного запаса
    ✨ Звуко-буквенный анализ слова
    ✨ Формирование грамотности
    ✨ Развитие фонематического слуха
    ✨ Развитие выразительности связной речи (учим детей давать полные развернутые ответы)

✍️ ПИСЬМО:
    ✨ Развитие мелкой моторики
    ✨ Постановка руки
    ✨ Развитие зрительного анализа
    ✨ Письмо под диктовку (на слух)

📝 Программа построена так, что на каждом занятии мы развиваем память, внимание и умение концентрироваться на одном виде деятельности, произвольность, умение наблюдать, сравнивать, и выделять главное, умение работать в группе.

⏱️ Занятия проходят в мини-группах до 6 человек 3 раза в неделю по 55 минут.

💰 Стоимость 1 занятия – 400р (абонементная система оплаты – за месяц вперед по количеству занятий)
        """
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=reply_markup
        )

    elif query.data == "onas":
        keyboard = [[InlineKeyboardButton("🔹Наши специалисты", callback_data="prepodi")],
        [InlineKeyboardButton("🔹Наш адрес", callback_data="adress")],
        [InlineKeyboardButton("🔹Часы работы", callback_data="rabot")],
        [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = """Дорогие друзья! 🤗

Наша замечательная команда «УМняшки» 🙌 во главе с талантливым основателем и руководителем Анной Валерьевной Евсейченко с радостью 😊 приветствует вас!

В нашей уютной детской студии детки от 2-х лет получают гармоничное всестороннее развитие. 🧑‍🎓 Занятия направлены как на коррекцию, так и на общее образование.

Учитывая важность развития речи в современном мире, все наши занятия проводятся с логопедическим уклоном. 🗣️ Для наших юных учеников упражнения и задания представлены в увлекательной игровой форме. 🎢

Мы рады пригласить вас и ваших детей стать частью нашей дружной семьи «УМняшек»! 👨‍👩‍👦‍👦"""
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text = message,
            reply_markup=reply_markup
        )

    elif query.data == "prepodi":
        keyboard = [[InlineKeyboardButton("🔹логопед", callback_data="prepod1")],
                    [InlineKeyboardButton("🔹дефектолог", callback_data="prepod2")],
                    [InlineKeyboardButton("🔹Педагоги", callback_data="prepodi1")],
                    [InlineKeyboardButton("Вернуться назад 🔙", callback_data="onas")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = """Выберите нужного вам специалиста"""
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=reply_markup
        )
    
    elif query.data == "prepod1":
        with open('jpg/12.jpg', 'rb') as f1:
            photo1 = f1.read()
        keyboard = [[InlineKeyboardButton("Вернуться назад 🔙", callback_data="prepodi")],
            [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = """Меня зовут Евсейченко Анна Валерьевна, я логопед. 
Закончила Южный Федеральный Университет города Ростов-на-Дону, факультет "Специальное (дефектологическое) образование". Учась на 2-ом курсе я поняла, что правильно выбрала профессию и логопедия - это моя судьба! Поняла, что хочу и могу помогать людям, и, по сей день - это моя жизненная миссия! 

Несмотря на то, что давно получила диплом и покинула стены университета, постоянно продолжаю учиться, т.к. в этой профессии часто появляются новые методы, инструменты, игры. Нужно всегда быть в "теме", чтобы быстрее и эффективнее добиваться результата."""
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo1,
            caption=message,
            reply_markup=reply_markup
        )

    elif query.data == "prepod2":
        with open('jpg/13.jpg', 'rb') as f1:
            photo1 = f1.read()
        keyboard = [[InlineKeyboardButton("Вернуться назад 🔙", callback_data="prepodi")],
            [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        context.bot.send_media_group(
            chat_id=update.effective_chat.id,
            media=[
                InputMediaPhoto(photo1)
            ],
        )
        message = """Я Ложаева Ирина Игоревна, и я дефектолог-психолог со специальным (дефектологическим) и психолого-педагогическим образованием. Выпускница Волгоградского Государственного Социально-Педагогического Университета одноименного города Волгограда, факультеты "Социально-коррекционная педагогика" и "Школьная психология". Всегда любила учиться и изучать новое, поэтому одного дефектологического образования для понимания полноты картины мне показалось мало, и только после получения двух "высших" поняла, что сделала правильный выбор. Такой осознанный подход спустя несколько лет прочно укоренил меня в своем выборе, что определил путь развития, цель которого – помогать растить здоровое и всесторонне развитое будущее поколение.

Дефектология, как наука, дала мне необходимую базу знаний для дальнейшего углубленного обучения практической логопедии, поэтому сейчас активно осваиваю новые горизонты.🌐 Логопедия оказалась вовсе не чуждой, напротив – понятной и знакомой.

Но, как Вы поняли, останавливаться на достигнутом не в моих интересах!"""
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=reply_markup
        )

    elif query.data == "prepodi1":
        keyboard = [[InlineKeyboardButton("🔹Сударкина Виктория Александровна", callback_data="prepod3")],
                    [InlineKeyboardButton("🔹", callback_data="prepod4")],
                    [InlineKeyboardButton("Вернуться назад 🔙", callback_data="prepodi")],
                    [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = """Выберите нужного вам специалиста"""
        context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=message,
            reply_markup=reply_markup
        )

    elif query.data == "prepod3":
        with open('jpg/14.jpg', 'rb') as f1:
            photo1 = f1.read()
        keyboard = [[InlineKeyboardButton("Вернуться назад 🔙", callback_data="prepodi")],
            [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = """Здравствуйте, меня зовут  Сударкина Виктория Александровна. Я учитель начальных классов и преподаватель дошкольного образования.  Закончила Каменский Педагогический Колледж.  
Мечтала быть учителем с самого детства. Считаю, чтобы обучение было продуктивным оно должно быть интересным!"""
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo1,
            caption=message,
            reply_markup=reply_markup
        )
    
    elif query.data == "prepod4":
        with open('jpg/15.jpg', 'rb') as f1:
            photo1 = f1.read()
        keyboard = [[InlineKeyboardButton("Вернуться назад 🔙", callback_data="prepodi")],
            [InlineKeyboardButton("Вернуться в меню 🏠", callback_data="next")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        message = """В разработке"""
        context.bot.send_photo(
            chat_id=update.effective_chat.id,
            photo=photo1,
            caption=message,
            reply_markup=reply_markup
        )

def send_message_to_all(update, context):
    # Проверяем, что сообщение отправлено администратором
    if update.message.chat.username not in ADMIN_USERNAMES:
        update.message.reply_text("У вас нет прав для отправки рассылки.")
        return

    # Получаем текст сообщения после команды "/sendtoall"
    message_parts = update.message.text.split(maxsplit=1)
    if len(message_parts) > 1:
        broadcast_message = message_parts[1].strip()
        
        # Проверяем, что сообщение не пустое
        if broadcast_message:
            users = get_all_users()
            for user_id in users:
                try:
                    context.bot.send_message(chat_id=user_id, text=broadcast_message)
                except Exception as e:
                    update.message.reply_text(f"Произошла ошибка при отправке сообщения пользователю {user_id}: {e}")

            update.message.reply_text("Мамочка, рассылка успешно отправлена)")
        else:
            update.message.reply_text("Мам, добавь текст после команды /love.")
    else:
        update.message.reply_text("Мам, добавь текст после команды /love.")


def photo_handler(update, context):
    # Проверяем, что пользователь является администратором
    if update.message.chat.username not in ADMIN_USERNAMES:
        return

    # Получаем файл фото
    photo_file = update.message.photo[-1].get_file()
    
    # Сохраняем фото на диск
    photo_file.download("photo.jpg")
    
    # Отправляем фото всем пользователям
    users = get_all_users()
    for user_id in users:
        try:
            with open("photo.jpg", "rb") as f:
                context.bot.send_photo(chat_id=user_id, photo=f)
        except Exception as e:
            update.message.reply_text(f"Произошла ошибка при отправке фото пользователю {user_id}: {e}")
    
    # Отправляем подтверждение пользователю
    update.message.reply_text("Мамочка, все получили фотографию")


import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def get_connection_and_cursor():
    try:
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS users
                    (username TEXT, first_name TEXT, last_name TEXT)''')
        return conn, c
    except sqlite3.Error as e:
        logging.error(f'Error connecting to the database: {e}')
        return None, None

# Функция для получения списка всех пользователей
def fetch_all_users(cursor):
    try:
        cursor.execute("SELECT username, first_name, last_name FROM users")
        return cursor.fetchall()
    except sqlite3.Error as e:
        logging.error(f'Error getting users from the database: {e}')
        return []

# Функция для добавления пользователя в базу данных
def insert_user(cursor, connection, username, first_name, last_name):
    try:
        if not user_exists(cursor, username):
            cursor.execute("INSERT INTO users (username, first_name, last_name) VALUES (?, ?, ?)", (username, first_name, last_name))
            connection.commit()
    except sqlite3.Error as e:
        logging.error(f'Error adding user to the database: {e}')

# Функция, обрабатывающая команду "/users"
def handle_users_command(update, context):
    if update.message.chat.username not in ADMIN_USERNAMES:
        update.message.reply_text("У вас нет прав для просмотра списка пользователей.")
        return

    connection, cursor = get_connection_and_cursor()
    if connection and cursor:
        users = fetch_all_users(cursor)
        if users:
            message = "Список пользователей:\n\n"
            for user in users:
                message += f"Username: @{user[0]}\nИмя: {user[1]}\nФамилия: {user[2]}\n\n"
            context.bot.send_message(chat_id=update.effective_chat.id, text=message)
        else:
            context.bot.send_message(chat_id=update.effective_chat.id, text="Нет зарегистрированных пользователей.")
        connection.close()
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Ошибка подключения к базе данных.")

# Функция для проверки, существует ли пользователь в базе данных
def user_exists(cursor, username):
    try:
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        return cursor.fetchone() is not None
    except sqlite3.Error as e:
        logging.error(f'Error checking if user exists in the database: {e}')
        return False

def create_database():
    conn = sqlite3.connect('promo_codes.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS promo_codes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT, chat_id INTEGER, username TEXT, first_name TEXT, last_name TEXT, promo_code TEXT)''')
    conn.commit()
    conn.close()

def generate_promo_code(chat_id, username, first_name, last_name):
    create_database()
    conn = sqlite3.connect('promo_codes.db')
    c = conn.cursor()

    # Проверяем, есть ли уже промокод для данного пользователя
    c.execute("SELECT promo_code FROM promo_codes WHERE chat_id = ?", (chat_id,))
    result = c.fetchone()
    if result:
        conn.close()
        return result[0]
    
    # Генерируем новый промокод
    characters = string.ascii_uppercase + string.digits
    promo_code = ''.join(secrets.choice(characters) for i in range(8))
    
    # Сохраняем промокод, username, first_name и last_name в базу данных
    c.execute("INSERT INTO promo_codes (chat_id, username, first_name, last_name, promo_code) VALUES (?, ?, ?, ?, ?)", (chat_id, username, first_name, last_name, promo_code))
    conn.commit()
    conn.close()
    
    return promo_code

def get_promo_codes(update, context):
    # Проверяем, является ли пользователь администратором
    username = update.effective_user.username
    if username not in ADMIN_USERNAMES:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Извините, у вас нет доступа к этой команде.")
        return

    # Получаем все записи из базы данных
    create_database()
    conn = sqlite3.connect('promo_codes.db')
    c = conn.cursor()
    c.execute("SELECT username, first_name, last_name, promo_code FROM promo_codes")
    rows = c.fetchall()
    conn.close()

    # Формируем сообщение с данными из базы данных
    message = "Все промокоды:\n\n"
    for row in rows:
        message += f"Имя пользователя: @{row[0]}\n"
        message += f"Имя: {row[1]}\n"
        message += f"Фамилия: {row[2]}\n"
        message += f"Промокод: {row[3]}\n\n"

    context.bot.send_message(chat_id=update.effective_chat.id, text=message)


def main():
    updater = Updater(token='7501173830:AAFoC2yVOYveCmaTPjYhsTl4eiQ13LJ-mws', use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(CallbackQueryHandler(next_message, pattern='^next$'))  
    dispatcher.add_handler(CallbackQueryHandler(handle_callback))
    dispatcher.add_handler(CommandHandler('promo', get_promo_codes))
    dispatcher.add_handler(CommandHandler('users', handle_users_command))
    send_to_all_handler = CommandHandler('love', send_message_to_all)
    dispatcher.add_handler(MessageHandler(Filters.photo, photo_handler))
    dispatcher.add_handler(send_to_all_handler)
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
