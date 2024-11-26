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
day = datetime.now().day                                                                            # День (Лол я хз как это описать)
mailing_users = []

#---------------------------------------------------------------------------------------------- Функции ----------------------------------------------------------------------------------------------

@bot.message_handler(commands=["start"])                                                            # Действия при вводе команды старт
def greeting(message):                                                                                  # Функция (принимает переменную типа message) 
    bot.send_message(message.chat.id, GREETING_TEXT, reply_markup=keyboard(GREETING_BUTTONS))               # Отправка приветствия вместе с кнопками
    bot.register_next_step_handler(message, distribution)
                                                                                       

def distribution(message):                                                                              # Функция (принимает переменную типа message) 
    global day                                                                                              # Получение доступа к переменной извне
    if(message.text==GREETING_BUTTONS[0] or message.text==FORTUNE_TELLING_BUTTONS[0]):                      # Проверка текста сообщения
        if(datetime.now().day!=day):                                                                            # Условие которое очищает список количества использований если наступает новый день
            user_limit.clear()                                                                                      # Очистка списка
            day = datetime.now().day                                                                                # Замена прошлой даты на новую
        if(user_limit.count(str(message.chat.id))<day_limit):                                                   # Если пользователь использовал функцию меньше day_limit раз то отправляет ему предсказание
            bot.send_message(message.chat.id, choice(fortune_telling)+"\n"+choice(fortune_telling), 
                             reply_markup=keyboard(FORTUNE_TELLING_BUTTONS+DISTRIBUTION_BUTTONS))                   # Отправка сообщения с предсказанием
            user_limit.append(str(message.chat.id))                                                                 # Добавление информации о том что пользователь еще раз использовал команду 
        else:                                                                                                   # Иначе (ебанарот тут реально надо это объяснять...)
            bot.send_message(message.chat.id, FORTUNE_TELLING_LIMIT_TEXT, 
                             reply_markup=keyboard(DISTRIBUTION_BUTTONS))                                           # Отправка сообщения 
        bot.register_next_step_handler(message, distribution)
            
    elif(message.text==GREETING_BUTTONS[1]):                                                                # Проверка текста сообщения
        bot.send_message(message.chat.id, choice(QUESTION_TEXT), reply_markup=keyboard(DISTRIBUTION_BUTTONS))      # Сообщение с вопросом
        bot.register_next_step_handler(message, question)

    elif(message.text==GREETING_BUTTONS[2]):                                                                # Проверка текста сообщения
        if(str(message.chat.id) in mailing_users):
            bot.send_message(message.chat.id, MAILING_TEXT, reply_markup=keyboard([MAILING_BUTTONS[1]]+DISTRIBUTION_BUTTONS))            
        else:
            bot.send_message(message.chat.id, MAILING_TEXT, reply_markup=keyboard([MAILING_BUTTONS[0]]+DISTRIBUTION_BUTTONS))
        bot.register_next_step_handler(message, mailing)

    elif(message.text==GREETING_BUTTONS[3]):                                                                # Проверка текста сообщения
        bot.send_message(message.chat.id, INFO_TEXT, reply_markup=keyboard(INFO_BUTTONS+DISTRIBUTION_BUTTONS))            
        bot.register_next_step_handler(message, info)

    else:   
        bot.send_message(message.chat.id, GREETING_TEXT, reply_markup=keyboard(GREETING_BUTTONS))
        bot.register_next_step_handler(message, distribution)


def info(message):
    if(message.text==DISTRIBUTION_BUTTONS[0]):   
        bot.send_message(message.chat.id, GREETING_TEXT, reply_markup=keyboard(GREETING_BUTTONS))
        bot.register_next_step_handler(message, distribution)

    elif(message.text==INFO_BUTTONS[0]): 
        bot.send_message(message.chat.id, INFO_CREW_TEXT, reply_markup=keyboard(INFO_CREW_BUTTONS+DISTRIBUTION_BUTTONS))
        bot.register_next_step_handler(message, info_crew)

    elif(message.text==INFO_BUTTONS[1]): 
        bot.send_message(message.chat.id, INFO_BAND_TEXT, reply_markup=keyboard(INFO_BAND_BUTTONS+DISTRIBUTION_BUTTONS))
        bot.register_next_step_handler(message, info_band)

    else:
        bot.send_message(message.chat.id, PRESS_BUTTON_TEXT, reply_markup=keyboard(INFO_BUTTONS+DISTRIBUTION_BUTTONS))            
        bot.register_next_step_handler(message, info)


def info_crew(message):
    if(message.text==DISTRIBUTION_BUTTONS[0]):   
        bot.send_message(message.chat.id, GREETING_TEXT, reply_markup=keyboard(GREETING_BUTTONS))
        bot.register_next_step_handler(message, distribution)
    
    elif(message.text==INFO_CREW_BUTTONS[0]): 
        bot.send_message(message.chat.id, INFO_CREW_CONTACT_TEXT, reply_markup=keyboard(DISTRIBUTION_BUTTONS))
        bot.register_next_step_handler(message, distribution)

    elif(message.text==INFO_CREW_BUTTONS[1]): 
        bot.send_message(message.chat.id, INFO_CREW_ONFIRE_TEXT, reply_markup=keyboard(DISTRIBUTION_BUTTONS))
        bot.register_next_step_handler(message, distribution)

    elif(message.text==INFO_CREW_BUTTONS[2]): 
        bot.send_message(message.chat.id, INFO_CREW_HELP_TEXT, reply_markup=keyboard(DISTRIBUTION_BUTTONS))
        bot.register_next_step_handler(message, distribution)

    else:
        bot.send_message(message.chat.id, PRESS_BUTTON_TEXT, reply_markup=keyboard(INFO_CREW_BUTTONS+DISTRIBUTION_BUTTONS))
        bot.register_next_step_handler(message, info_crew)


def info_band(message):
    if(message.text==DISTRIBUTION_BUTTONS[0]):   
        bot.send_message(message.chat.id, GREETING_TEXT, reply_markup=keyboard(GREETING_BUTTONS))
        bot.register_next_step_handler(message, distribution)

    elif(message.text==INFO_BAND_BUTTONS[0]):
        bot.send_message(message.chat.id, INFO_BAND_LINK_TEXT, reply_markup=keyboard(DISTRIBUTION_BUTTONS))
        bot.register_next_step_handler(message, distribution)

    elif(message.text==INFO_BAND_BUTTONS[1]):
        bot.send_message(message.chat.id, INFO_BAND_EVENTS_TEXT, reply_markup=keyboard(DISTRIBUTION_BUTTONS))
        bot.register_next_step_handler(message, distribution)

    else:
        bot.send_message(message.chat.id, PRESS_BUTTON_TEXT, reply_markup=keyboard(INFO_BAND_BUTTONS+DISTRIBUTION_BUTTONS))
        bot.register_next_step_handler(message, info_band)


def mailing(message):
    if(message.text==DISTRIBUTION_BUTTONS[0]):   
        bot.send_message(message.chat.id, GREETING_TEXT, reply_markup=keyboard(GREETING_BUTTONS))
        bot.register_next_step_handler(message, distribution)

    elif(message.text==MAILING_BUTTONS[0]):   
        bot.send_message(message.chat.id, MAILING_STАRT_TEXT, reply_markup=keyboard(DISTRIBUTION_BUTTONS))
        mailing_users.append(str(message.chat.id))
        bot.register_next_step_handler(message, distribution)

    elif(message.text==MAILING_BUTTONS[1]):   
        bot.send_message(message.chat.id, MAILING_END_TEXT, reply_markup=keyboard(DISTRIBUTION_BUTTONS))
        mailing_users.remove(str(message.chat.id))
        bot.register_next_step_handler(message, distribution)

    else:
        if(str(message.chat.id) in mailing_users):
            bot.send_message(message.chat.id, PRESS_BUTTON_TEXT, reply_markup=keyboard([MAILING_BUTTONS[1]]+DISTRIBUTION_BUTTONS))            
        else:
            bot.send_message(message.chat.id, PRESS_BUTTON_TEXT, reply_markup=keyboard([MAILING_BUTTONS[0]]+DISTRIBUTION_BUTTONS))
        bot.register_next_step_handler(message, mailing)


def question(message):
    if(message.text==DISTRIBUTION_BUTTONS[0]):   
        bot.send_message(message.chat.id, GREETING_TEXT, reply_markup=keyboard(GREETING_BUTTONS))
    else:
        bot.send_message(message.chat.id, "Ответ на вопрос)", reply_markup=keyboard(DISTRIBUTION_BUTTONS))

    bot.register_next_step_handler(message, distribution)


def keyboard(button=[]):                                                                            # Функция принимает массив строк (которые будут служить названиями следующих кнопок)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)                                            # Создание маркапа
    for i in range(len(button)):                                                                        # Цикл проходящий по всем элементам массива button
        markup.add(types.KeyboardButton(button[i]))                                                         # Добавление кнопки
    return markup                                                                                       # Возвращение маркапа
# Функция создающая кнопки для бота

bot.infinity_polling()                                                                              # Функция благодаря которой бот непрерывно работает