'''
    Комменты и код полностью написаны мной (Cectus4)
    По вопросам тг:@cectus1
'''

import telebot
from config import *
from telebot import types
# Импорт нужных библиотек и конфига

bot = telebot.TeleBot(BOT_TOKEN) # Бот токен служит для связи бота с апи телеграма (Его берем из конфига)
# Иницилизация бота

@bot.message_handler(commands=["start"]) # Объявляем что нижеобъявленная функция будет выполняться при введении 
def greetings(message): # Функция (принимает переменную типа message)
    bot.send_message(message.chat.id, ":)")
# Действия при вводе команды старт



def keyboard(button=[]):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True) # Создание маркапа
    for i in range(len(button)): # Цикл проходящий по всем элементам массива button
        markup.add(types.KeyboardButton(button[i])) # Добавление кнопки
    return markup # Возвращение маркапа
# Функция создающая кнопки для бота

bot.infinity_polling()