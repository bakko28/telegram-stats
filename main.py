import telebot
import sqlite3
from telebot import types 
from datetime import datetime

bot = telebot.TeleBot('7122079884:AAHXd98FRmrHMf7mqHwysxza0Hs_6930yWE')

@bot.message_handler(commands=['start'])
def start_message(message):
    markup_create_table = types.InlineKeyboardMarkup()
    create_table = types.InlineKeyboardButton("Создать таблицу", callback_data='create_table')
    markup_create_table.add(create_table)

    markup_table_list = types.InlineKeyboardMarkup()
    table_list = types.InlineKeyboardButton("Список таблиц", callback_data='table_list')
    markup_table_list.add(table_list)

    user_id = message.from_user.id
    username = message.from_user.username
    current_date = datetime.now()
    date = current_date.strftime("%d.%m.%Y")

    bot.send_message(message.chat.id, f'Привет {username}')

    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id FROM users')
    ids = cursor.fetchall()
    id_list = [row[0] for row in ids]

    if user_id in id_list:
        print(f'Пользователь найден: {user_id}')
        bot.send_message(message.chat.id, 'Вижу мы уже с вами работали. Хотите продолжить?', reply_markup=markup_table_list)
    else:
        print(f'Пользователь {user_id} не найден. Начинаю добавление в базу данных.')
        cursor.execute(''' INSERT INTO users (id, username, date, tables) VALUES (?, ?, ?, ?)
            ''', (user_id, username, date, 0))

        conn.commit()
        print(f'Добавил пользователя {user_id} в базу данных.')
        bot.send_message(message.chat.id, 'Первый раз пользуетесь ботом? Давай начнем с создания таблицы.', reply_markup=markup_create_table)
    
    conn.close()

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == 'create_table':
        bot.send_message(call.message.chat.id, 'Давайте поподробнее расскажу про создание таблицы. \n\n Вот небольшой пример создания: \n day TEXT,\n reed_book INT,\n gym_time INT,\n sleep_time INT,')
    elif call.data == 'table_list':
        bot.send_message(call.message.chat.id, 'Вы выбрали список таблиц.')


bot.polling()