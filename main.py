import telebot
from sql import article_db
from keyboards import *
from bs4 import BeautifulSoup
import requests as rq
from sd_parser import *
from fake_headers import Headers
from random import choice, randint
from const import *
from text import text
from os import getcwd
from datetime import datetime
#from time import time
import mysql.connector as sql
from sql import *


header = Headers(
    browser="chrome",  # Generate only Chrome UA
    os="win",  # Generate ony Windows platform
    headers=True  # generate misc headers
)

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def main(message):
    new_day=False
    if new_day:
        reboot_count_sended_today()

    # register for new users
    if message.json['from']['id'] not in user_db.get_users_id():
        user_db.create(message.json['from']['id'])
        bot.send_message(message.chat.id, text['greet_for_beginner'], reply_markup=keyboard.main())
    else:
        sent = bot.send_message(message.chat.id, choice(text['greet']), reply_markup=keyboard.main())
    bot.register_next_step_handler(sent, menu_selector)

#Inline keyboard callback
@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):


    bot.answer_callback_query(callback_query_id=call.id, text=choice(text['rated_callback']))

    mark = float(call.data.split()[0])
    theme = call.data.split()[1:-1]
    article_id = call.data.split()[-1]

    if '&' in theme:
        del (theme[1])
        theme = '_'.join([i.lower() for i in theme])
    else:
        theme = '_'.join([i.lower() for i in theme])

    article_db.rate(article_id, mark)
    user_db.update_count_rated(call.from_user.id, mark)
    user_db.rate(call.from_user.id, theme, mark)
    user_db.add_view(call.from_user.id, article_id, mark)


def settings(message):
    if message.text == '🧨Сбросить рекомендации':
        user_db.reboot_coefs(message.chat.id)
        sent = bot.send_message(message.chat.id, text['reboot'], reply_markup=keyboard.main())
        bot.register_next_step_handler(sent, menu_selector)
    elif message.text == '🧠Сбросить статистику':
        user_db.reboot_counters(message.chat.id)
        sent = bot.send_message(message.chat.id, text['reboot'], reply_markup=keyboard.main())
        bot.register_next_step_handler(sent, menu_selector)
    elif message.text == 'Статистика':

        ID = message.json['from']['id']
        stat_text = f'Просмотрено статей за сегодня: {user_db.get_count_sended_today(ID)}\n\n' \
                    f'😎Всего поставлено Положительно: {user_db.get_count_rated(ID)["count_likes"]}\n\n' \
                    f'😐Всего поставлено Нейтрально: {user_db.get_count_rated(ID)["count_neutral"]}\n\n' \
                    f'😢Всего поставлено Отрицательно: {user_db.get_count_rated(ID)["count_dislikes"]}\n\n' \
                    f'Просмотрено всего: {user_db.get_count_sended_total(ID)}\n\n' \
                    f'Любимая тема: {user_db.get_favourite_theme(ID)}\n\n' \
                    f'Нелюбимая тема: {user_db.get_negative_theme(ID)}\n\n\n' \
                    f'🥅Хотите поставить цель?\n'
        sent = bot.send_message(message.chat.id, stat_text, reply_markup=keyboard.settings())
        bot.register_next_step_handler(sent, settings)

    elif message.text == 'Назад':
        sent = bot.send_message(message.chat.id, text['back'], reply_markup=keyboard.main())
        bot.register_next_step_handler(sent, menu_selector)
    else:
        sent = bot.send_message(message.chat.id, text['wrong'], reply_markup=keyboard.settings())
        bot.register_next_step_handler(sent, settings)


@bot.message_handler(func=lambda message: True)
def menu_selector(message):
    if message.text == '📤Получить статью':
        user_db.update_count_viewed(message.chat.id)
        try:
            theme = choice(theme_most_liked(3))
            if len(theme.split(' & ')) == 1:  # 'living well' case
                root = '_'.join(theme.lower().split(' & ').split())
            else:
                root = '_'.join(theme.lower().split(' & '))
            with open(f"{root}.txt", 'r') as f:

                item = eval(choice(f.read().splitlines()[1:]))
            # IndexError as ValueError
        except Exception as e:
            print(e)
            sent = bot.send_message(message.chat.id, text['warning'])
            with open(f"top.txt", 'r') as f2:
                item = eval(choice(f2.read().splitlines()[1:]))

            sent = bot.send_message(message.chat.id,
                                    f"📬{item['name']}\n\n🗓{item['description']['date']}\n🏫{item['description']['source']}\n\n💻Версия  для удобного чтения c компьютера:\n{get_telegraph(item)}\n\n{item['url']}",
                                    reply_markup=keyboard.rate(list(item['themes'].keys())[0]))
            # add a new theme if it doesnt exist before
            if list(item['themes'].keys())[0] not in themes["name"]:
                add_theme(list(item['themes'].keys())[0], 0)

            related_sended.append(item['url'])

            sent = bot.send_message(message.chat.id, text['back'], reply_markup=keyboard.main())
            bot.register_next_step_handler(sent, menu_selector)

    elif message.text == '⚖Калибровка':
        id = message.chat.id
        sent = bot.send_message(id, text['calibration'], reply_markup=keyboard.main())
        user_db.reboot_related_sended(id)
        calibration_articles = article_db.calibration(id)
        user_db.add_related_sended(message.chat.id, [i[0] for i in calibration_articles])
        for article in calibration_articles:
            bot.send_message(id, article_db.decorate_article(article[0]), reply_markup=keyboard.rate(article[1], article[0]))

        bot.register_next_step_handler(sent, menu_selector)

    elif message.text == '⏰Рассылка':
        sent = bot.send_message(message.chat.id, text['auto'], reply_markup=keyboard.main())
        bot.register_next_step_handler(sent, menu_selector)
    elif message.text == '⚙Настройки':
        sent = bot.send_message(message.chat.id, text['settings'], reply_markup=keyboard.settings())
        bot.register_next_step_handler(sent, settings)

    elif message.text == 'Источники':
        sent = bot.send_message(message.chat.id, text['sources'], reply_markup=keyboard.main())
        bot.register_next_step_handler(sent, menu_selector)

    else:
        sent = bot.send_message(message.chat.id, text['wrong'], reply_markup=keyboard.main())
        bot.register_next_step_handler(sent, menu_selector)


bot.polling()
