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
from time import time
import mysql.connector as sql
from sql import *

# ----------------------------------------------------------------------------------------------------------------------#
# themes = {"name": [], "rating": []}
header = Headers(
    browser="chrome",  # Generate only Chrome UA
    os="win",  # Generate ony Windows platform
    headers=True  # generate misc headers
)


# ----------------------------------------------------------------------------------------------------------------------#
def theme_most_liked(count):
    final = []
    deleted = []
    # list(set(themes['rating']) - set(deleted))
    for i in range(count):
        index = themes['rating'].index(max(list(set(themes['rating']) - set(deleted))))
        final.append(themes['name'][index])
        deleted.append(themes['rating'][index])
    return final


# -------------------------------------------------------BOT------------------------------------------------------------#

bot = telebot.TeleBot(TOKEN)


# # article_db.update_content()
# user_db.create_views()


@bot.message_handler(commands=['start'])
def main(message):
    sent = bot.send_message(message.chat.id, text['greet'], reply_markup=keyboard.main())

    # register for new users
    if message.chat.id not in user_db.get_users_id():
        user_db.create(message.chat.id)

    bot.register_next_step_handler(sent, menu_selector)


# многоразовый отклик на кнопки в клаве
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
        with open("stats.txt", 'r') as f:
            if f.read().splitlines()[0] != datetime.now().strftime("%d-%m-%Y"):
                reboot_count_sended_today()
        stat_text = f'Просмотрено статей за сегодня: {get_count_sended_today()}\n' \
                    f'😎Всего поставлено Положительно: {get_count_rated()[0]}\n' \
                    f'😐Всего поставлено Нейтрально: {get_count_rated()[1]}\n' \
                    f'😢Всего поставлено Отрицательно: {get_count_rated()[2]}\n' \
                    f'Просмотрено всего: {get_count_sended_total()}\n' \
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
        for elem in calibration_articles:
            bot.send_message(id, article_db.decorate_article(elem[0]), reply_markup=keyboard.rate(elem[1], elem[0]))

        bot.register_next_step_handler(sent, menu_selector)

    elif message.text == '⏰Рассылка':
        sent = bot.send_message(message.chat.id, text['auto'], reply_markup=keyboard.main())
        bot.register_next_step_handler(sent, menu_selector)
    elif message.text == '⚙Настройки':
        sent = bot.send_message(message.chat.id, text['settings'], reply_markup=keyboard.settings())
        bot.register_next_step_handler(sent, settings)
    else:
        sent = bot.send_message(message.chat.id, text['wrong'], reply_markup=keyboard.main())
        bot.register_next_step_handler(sent, menu_selector)


bot.polling()
