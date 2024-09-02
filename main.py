import telebot
import sqlite3
from datetime import datetime
from telebot import types

bot = telebot.TeleBot('7122079884:AAHXd98FRmrHMf7mqHwysxza0Hs_6930yWE')

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, f'Привет, {message.from_user.username}. \n\n Я бот созданный для помощи тебе в саморазвитии.')

    current_date = datetime.now()
    formatted_date = current_date.strftime("%d.%m.%Y")

    check_user_on_db(message.from_user.id, message.from_user.username, formatted_date, message)
    

@bot.message_handler(func=lambda message: True)
def add_on_db_message(message):
    markup = types.InlineKeyboardMarkup()
    create_table = types.InlineKeyboardButton("Создать таблицу", callback_data='create_table')
    markup.add(create_table)
    bot.send_message(message.chat.id, 'Вижу ты новенький. Я добавил тебя в базу данных и предлагаю создать тебе свою первую таблицу с привычками.', reply_markup=markup)

def old_user_message(message):
    markup = types.InlineKeyboardMarkup()
    table_list = types.InlineKeyboardButton("Список таблиц", callback_data='table_list')
    markup.add(table_list)
    bot.send_message(message.chat.id, 'Вижу ты уже работал со мной. Давай посмотрим на твои старые таблицы.', reply_markup=markup)

def echo_all(message):
    bot.reply_to(message, "Ваше сообщение сохранено в базе данных.")

def check_user_on_db(user_id, username, date, message):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users')
    ids = cursor.fetchall()
    id_list = [row[0] for row in ids]
    print(id_list)

    conn.close()

    if user_id in id_list:
        print('Пользователь найден')
        old_user_message(message)
    else:
        print('Пользователь не найден')
        add_user(user_id, username, date)
        add_on_db_message(message)

def add_user(id, username, date):
    print(id, username, date, 0)
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('''
    INSERT INTO users (id, username, date, tables) VALUES (?, ?, ?, ?)
    ''', (id, username, date, 0))

    conn.commit()

bot.polling()
