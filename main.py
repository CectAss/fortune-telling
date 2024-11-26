'''
    Комменты и код полностью написаны мной (Cectus4)
    По вопросам тг: @cectus1
'''

import telebot
from config import *
from telebot import types
from datetime import datetime
# Импорт нужных библиотек и конфига

bot = telebot.TeleBot(BOT_TOKEN)                                                                    # Бот токен служит для связи бота с апи телеграма (Его берем из конфига)
# Иницилизация бота

user_limit = []                                                                                     # Локальный список с количеством использованний за день
day = 25                                                                                            # День (Лол я хз как это описать)


@bot.message_handler(commands=["start"])
def greeting(message):
    bot.send_message(message.chat.id, GREETING_TEXT, reply_markup=keyboard(GREETING_BUTTONS))


@bot.message_handler(commands=["test"])                                                             # Объявляем что нижеобъявленная функция будет выполняться при введении команды /start
def test(message):                                                                                  # Функция (принимает переменную типа message)
    if(datetime.now().day!=day):                                                                    # Условие которое очищает список количества использований если наступает новый день
        user_limit.clear()                                                                          # Очистка списка
        day = datetime.now().day                                                                    # Замена прошлой даты на новую
    if(user_limit.count(str(message.chat.id))<3):                                                   # Если пользователь использовал функцию меньше 3 раз то отправляет ему предсказание
        bot.send_message(message.chat.id, ":)")                                                     # Отправка предсказания пользователю
        user_limit.append(str(message.chat.id))                                                     # Добавление информации о том что пользователь еще раз использовал команду 
    else:                                                                                           # Иначе (ебанарот тут реально надо это объяснять...)
        bot.send_message(message.chat.id, "Вы уже получили улыбочку 3 раза, приходите завтра!")     # Отправка сообщения о том что пользовтаель использовал свой дневной лимит предсказаний
# Действия при вводе команды старт



def keyboard(button=[]):                                                                            # Функция принимает массив строк (которые будут служить названиями следующих кнопок)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)                                        # Создание маркапа
    for i in range(len(button)):                                                                    # Цикл проходящий по всем элементам массива button
        markup.add(types.KeyboardButton(button[i]))                                                 # Добавление кнопки
    return markup                                                                                   # Возвращение маркапа
# Функция создающая кнопки для бота

bot.infinity_polling()                                                                              # Функция благодаря которой бот непрерывно работает