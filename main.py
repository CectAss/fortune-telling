#------------------------------------------------------------------------ Комменты и код полностью написаны мной (Cectus4), по вопросам тг: @cectus1 -----------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------- Имопрт библиотек и конфига----------------------------------------------------------------------------------------

import telebot                                                                                      # Импорт основной библиотеки для работы с АПИ телеграма
from config import *                                                                                # Импорт конфигов
from telebot import types                                                                           # Импорт types из библиотеки telebot
from datetime import datetime                                                                       # Библиотека для получении времени
from random import choice                                                                           # Библиотека для рандомизации

#---------------------------------------------------------------------------------------------- Инициальзация бота ----------------------------------------------------------------------------------------------


bot = telebot.TeleBot(BOT_TOKEN)                                                                    # Бот токен служит для связи бота с апи телеграма (Его берем из конфига)

#---------------------------------------------------------------------------------------------- Создание локальных переменных и чтение из файла ----------------------------------------------------------------------------------------------

with open("fortune-telling.txt") as file:
    fortune_telling = file.read().split("\n")
day_limit = 3                                                                                       # Дневной лимит предсказаний пользователя
user_limit = []                                                                                     # Локальный список с количеством использованний за день
day = 25                                                                                            # День (Лол я хз как это описать)

#---------------------------------------------------------------------------------------------- Функции ----------------------------------------------------------------------------------------------

@bot.message_handler(commands=["start"])                                                            # Действия при вводе команды старт
def greeting(message):                                                                                  # Функция (принимает переменную типа message) 
    bot.send_message(message.chat.id, GREETING_TEXT, reply_markup=keyboard(GREETING_BUTTONS))               # Отправка приветствия вместе с кнопками

                                                                                                    

@bot.message_handler(content_types=['text'])                                                        # Функция выполняющаяся при вводе любого текста 
def distribution(message):                                                                              # Функция (принимает переменную типа message) 
    global day                                                                                              # Получение доступа к переменной извне
    if(message.text==GREETING_BUTTONS[0]):                                                                  # Проверка текста сообщения
        if(datetime.now().day!=day):                                                                            # Условие которое очищает список количества использований если наступает новый день
            user_limit.clear()                                                                                      # Очистка списка
            day = datetime.now().day                                                                                # Замена прошлой даты на новую
        if(user_limit.count(str(message.chat.id))<day_limit):                                                   # Если пользователь использовал функцию меньше day_limit раз то отправляет ему предсказание
            bot.send_message(message.chat.id, choice(fortune_telling), 
                             reply_markup=keyboard(DISTRIBUTION_BUTTONS))                                           # Отправка сообщения с предсказанием
            user_limit.append(str(message.chat.id))                                                                 # Добавление информации о том что пользователь еще раз использовал команду 
        else:                                                                                                   # Иначе (ебанарот тут реально надо это объяснять...)
            bot.send_message(message.chat.id, FORTUNE_TELLING_LIMIT_TEXT, 
                             reply_markup=keyboard(DISTRIBUTION_BUTTONS))                                           # Отправка сообщения 
    elif(message.text==GREETING_BUTTONS[1]):                                                                # Проверка текста сообщения
        bot.send_message(message.chat.id, choice(QUESTION_TEXT), reply_markup=types.ReplyKeyboardRemove())              # Сообщение с вопросом
    elif(message.text==GREETING_BUTTONS[2]):                                                                # Проверка текста сообщения
        bot.send_message(message.chat.id, MAILING_TEXT, reply_markup=types.ReplyKeyboardRemove())               # Текст рассылки
    elif(message.text==GREETING_BUTTONS[3]):                                                                # Проверка текста сообщения
        bot.send_message(message.chat.id, INFO_TEXT, reply_markup=types.ReplyKeyboardRemove())                  # Текст о вас
    elif(message.text==GREETING_BUTTONS[4]):                                                                # Проверка текста сообщения
        bot.send_message(message.chat.id, MONEY_TEXT, reply_markup=types.ReplyKeyboardRemove())                 # Реквизиты
    elif(message.text==DISTRIBUTION_BUTTONS[0]):   
        bot.send_message(message.chat.id, GREETING_TEXT, reply_markup=keyboard(GREETING_BUTTONS))


def keyboard(button=[]):                                                                            # Функция принимает массив строк (которые будут служить названиями следующих кнопок)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)                                            # Создание маркапа
    for i in range(len(button)):                                                                        # Цикл проходящий по всем элементам массива button
        markup.add(types.KeyboardButton(button[i]))                                                         # Добавление кнопки
    return markup                                                                                       # Возвращение маркапа
# Функция создающая кнопки для бота

bot.infinity_polling()                                                                              # Функция благодаря которой бот непрерывно работает