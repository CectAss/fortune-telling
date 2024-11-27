#------------------------------------------------------------------------ Комменты и код полностью написаны мной (Cectus4), по вопросам тг: @cectus1 -----------------------------------------------------------------------------
#---------------------------------------------------------------------------------------------- Имопрт библиотек и конфига------------------------------------------------------------------------------------------------

import telebot                                                                                      # Импорт основной библиотеки для работы с АПИ телеграма
from config import *                                                                                # Импорт конфигов
from telebot import types                                                                           # Импорт types из библиотеки telebot
from datetime import datetime                                                                       # Библиотека для получении времени
from random import choice                                                                           # Библиотека для рандомизации
import threading

#---------------------------------------------------------------------------------------------- Инициальзация бота ----------------------------------------------------------------------------------------------------------

bot = telebot.TeleBot(BOT_TOKEN)                                                                    # Подключение к АПИ телеграма

#---------------------------------------------------------------------------------------------- Создание локальных переменных и чтение из файла ----------------------------------------------------------------------------------------------

with open("answers.txt") as file:                                                                   # Открытие файла с ответами
    answers = file.read().split("\n")                                                                   # Создание массива ответов
with open("fortune-telling.txt") as file:                                                           # Открытие файла с предсказаниями
    fortune_telling = file.read().split("\n")                                                           # Создание массива предсказаний
day_limit = 3                                                                                       # Дневной лимит предсказаний пользователя
user_limit = []                                                                                     # Локальный список с количеством использованний за день
fortune_telling_day = datetime.now().day                                                            # День (для дневного лимита) который помнит бот
mailing_day = datetime.now().day                                                                    # День (для рассылки) который помнит бот
mailing_users = []                                                                                  # Массив пользователей, подписаных на рассылку

#---------------------------------------------------------------------------------------------- Функции ----------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------- Старт ----------------------------------------------------------------------------------------------------------------------------------------------

@bot.message_handler(commands=["start"])                                                            # Объявляю что нижеупомянутая функция будет вызвана при команде /start
def greeting(message):                                                                              # Создание функции greeting
    bot.send_message(message.chat.id, GREETING_TEXT, reply_markup=keyboard(MAIN_BUTTONS))               # Отправка приветствия вместе с кнопками
    bot.register_next_step_handler(message, distribution)                                               # Редирект пользователя в функцию отвечающую за основные кнопки (см. функцию distribution)

#-------------------------------------------------------------------------------------------------- Основные кнопки ----------------------------------------------------------------------------------------------------------------------------------------------   

def distribution(message):                                                                          # Создание функции distribution
    global fortune_telling_day                                                                          # Получение доступа к переменной извне для дальнейшего изменения
    if(message.text==MAIN_BUTTONS[0] or message.text==FORTUNE_TELLING_BUTTONS[0]):                      # Если пользователь ввел любой запрос про гадание (MAIN_BUTTONS[0], FORTUNE_TELLING_BUTTONS[0])
        if(datetime.now().day!=fortune_telling_day):                                                        # Если день, который помнит бот не совпадает с сегодняшним днем
            user_limit.clear()                                                                                  # Очистка списка (обновление дневного лимита использования гадания) 
            fortune_telling_day = datetime.now().day                                                            # Замена даты, которую помнит бот на сегодняшню
        if(user_limit.count(str(message.chat.id))<day_limit):                                               # Если пользователь не привысил свой дневгой лимит гаданий
            bot.send_message(message.chat.id, choice(fortune_telling)+" "+choice(fortune_telling), 
                             reply_markup=keyboard(FORTUNE_TELLING_BUTTONS+DISTRIBUTION_BUTTONS))               # Отправка сообщения с предсказанием
            user_limit.append(str(message.chat.id))                                                             # Добавление информации о том что пользователь еще раз использовал команду 
        else:                                                                                               # Если пользователь использовал все свои запросы на гадание 
            bot.send_message(message.chat.id, FORTUNE_TELLING_LIMIT_TEXT, 
                             reply_markup=keyboard(DISTRIBUTION_BUTTONS))                                       # Отправка сообщения о том что пользователь сегодня больше не может получить предсказание
        bot.register_next_step_handler(message, distribution)                                               # Редирект в эту же функцию
            
    elif(message.text==MAIN_BUTTONS[1]):                                                                # Если пользователь ввел запрос про вопрос (MAIN_BUTTONS[1])
        bot.send_message(message.chat.id, choice(QUESTION_TEXT), 
                         reply_markup=keyboard(DISTRIBUTION_BUTTONS))                                          # Отправка сообщения спрашивающее ответ на что хочет узнать пользователь
        bot.register_next_step_handler(message, question)                                                      # Редирект пользователя в функцию отвечающую за вопросы (см. функцию question)

    elif(message.text==MAIN_BUTTONS[2]):                                                                # Если пользователь ввел запрос про рассылку (MAIN_BUTTONS[2])
        if(str(message.chat.id) in mailing_users):                                                          # Если пользователь уже подписан на рассылку
            bot.send_message(message.chat.id, choice(MAILING_TEXT), 
                             reply_markup=keyboard([MAILING_BUTTONS[1]]+DISTRIBUTION_BUTTONS))                  # Отправка информации о рассылке с кнопками отписки и базовой кнопки
        else:                                                                                               # Если пользователь еще не подписан на рассылку
            bot.send_message(message.chat.id, choice(MAILING_TEXT), 
                             reply_markup=keyboard([MAILING_BUTTONS[0]]+DISTRIBUTION_BUTTONS))                  # Отправка информации о рассылке с кнопками подписки и базовой кнопки
        bot.register_next_step_handler(message, mailing)                                                    # Редирект в функцию отвечающую за рассылку (см. функцию mailing)

    elif(message.text==MAIN_BUTTONS[3]):                                                                # Если пользователь ввел запрос про информацию
        bot.send_message(message.chat.id, INFO_TEXT,                                                        
                         reply_markup=keyboard(INFO_BUTTONS+DISTRIBUTION_BUTTONS))                          # Отправка сообщения с вопросом о чем хочет получить информацию пользователь
        bot.register_next_step_handler(message, info)                                                       # Редирект в функцию отвечающую за информацию (см. функцию info)

    else:                                                                                               # Если пользователь не нажал на кнопку и ввел что то свое   
        bot.send_message(message.chat.id, MAIN_TEXT,        
                         reply_markup=keyboard(MAIN_BUTTONS))                                               # Отправка сообщения заново
        bot.register_next_step_handler(message, distribution)                                               # Редирект в эту же функцию

#-------------------------------------------------------------------------------------------------- Обработка информации ----------------------------------------------------------------------------------------------------------------------------------------------   

def info(message):                                                                                  # Создание функции info                                                                            
    if(message.text==DISTRIBUTION_BUTTONS[0]):                                                          # Если пользователь нажал кнопку возврата в меню
        bot.send_message(message.chat.id, MAIN_TEXT, 
                         reply_markup=keyboard(MAIN_BUTTONS))                                               # Отправка приветствия с кнопками
        bot.register_next_step_handler(message, distribution)                                               # Редирект в основную функцию (см. функцию distribution)

    elif(message.text==INFO_BUTTONS[0]):                                                                # Если пользователь хочет узнать о крю
        bot.send_message(message.chat.id, INFO_CREW_TEXT, 
                         reply_markup=keyboard(INFO_CREW_BUTTONS+DISTRIBUTION_BUTTONS))                     # Отправка сообщения с выбором информации
        bot.register_next_step_handler(message, info_crew)                                                  # Редирект в функцию с информацией о крю (см. функцию info_crew)

    elif(message.text==INFO_BUTTONS[1]):                                                                # Если пользователь хочет узнать о группе
        bot.send_message(message.chat.id, INFO_BAND_TEXT, 
                         reply_markup=keyboard(INFO_BAND_BUTTONS+DISTRIBUTION_BUTTONS))                     # Отправка сообщения с выбором информации
        bot.register_next_step_handler(message, info_band)                                                  # Редирект в функцию с информацией о группе (см. функцию info_band)

    else:                                                                                               # Если пользователь не нажал на кнопку и ввел что то свое   
        bot.send_message(message.chat.id, PRESS_BUTTON_TEXT, 
                         reply_markup=keyboard(INFO_BUTTONS+DISTRIBUTION_BUTTONS))                          # Отправка сообщения с просьбой нажать на кнопку
        bot.register_next_step_handler(message, info)                                                       # Редирект в эту же функцию

#-------------------------------------------------------------------------------------------------- Обработка информации о крю ----------------------------------------------------------------------------------------------------------------------------------------------   

def info_crew(message):                                                                             # Создание функции info_crew
    if(message.text==DISTRIBUTION_BUTTONS[0]):                                                          # Если пользователь нажал кнопку возврата в меню
        bot.send_message(message.chat.id, MAIN_TEXT, 
                         reply_markup=keyboard(MAIN_BUTTONS))                                               # Отправка приветствия с кнопками
        bot.register_next_step_handler(message, distribution)                                               # Редирект в основную функцию (см. функцию distribution)
    
    elif(message.text==INFO_CREW_BUTTONS[0]):                                                           # Если пользователь хочет узнать контакты крю
        bot.send_message(message.chat.id, INFO_CREW_CONTACT_TEXT, 
                         reply_markup=keyboard(DISTRIBUTION_BUTTONS))                                       # Отправка сообщения с контактной информацией о группе
        bot.register_next_step_handler(message, distribution)                                               # Редирект в основную функцию (см. функцию distribution)

    elif(message.text==INFO_CREW_BUTTONS[1]):                                                           # Если пользователь хочет узнать что значит мы горим
        bot.send_message(message.chat.id, INFO_CREW_ONFIRE_TEXT, 
                         reply_markup=keyboard(DISTRIBUTION_BUTTONS))                                       # Отправка сообщения с информацией о горении
        bot.register_next_step_handler(message, distribution)                                               # Редирект в основную функцию (см. функцию distribution)

    elif(message.text==INFO_CREW_BUTTONS[2]):                                                           # Если пользователь хочет узнать о том как можно помочь группе
        bot.send_message(message.chat.id, INFO_CREW_HELP_TEXT,      
                         reply_markup=keyboard(DISTRIBUTION_BUTTONS))                                       # Отправка сообщения с информацией о помощи группе
        bot.register_next_step_handler(message, distribution)                                               #  Редирект в основную функцию (см. функцию distribution)

    else:                                                                                               # Если пользователь не нажал на кнопку и ввел что то свое  
        bot.send_message(message.chat.id, PRESS_BUTTON_TEXT, 
                         reply_markup=keyboard(INFO_CREW_BUTTONS+DISTRIBUTION_BUTTONS))                     # Отправка сообщения с просьбой нажать на кнопку
        bot.register_next_step_handler(message, info_crew)                                                  # Редирект в эту же функцию

#-------------------------------------------------------------------------------------------------- Обработка информации о группе ----------------------------------------------------------------------------------------------------------------------------------------------   

def info_band(message):                                                                             # Создание функции info_band
    if(message.text==DISTRIBUTION_BUTTONS[0]):                                                          # Если пользователь нажал кнопку возврата в меню
        bot.send_message(message.chat.id, MAIN_TEXT, 
                         reply_markup=keyboard(MAIN_BUTTONS))                                               # Отправка приветствия с кнопками
        bot.register_next_step_handler(message, distribution)                                               # Редирект в основную функцию (см. функцию distribution)

    elif(message.text==INFO_BAND_BUTTONS[0]):                                                           # Если пользователь хочет получить ссылки на группу
        bot.send_message(message.chat.id, INFO_BAND_LINK_TEXT, 
                         reply_markup=keyboard(DISTRIBUTION_BUTTONS))                                       # Отправка сообщения с ссылками на группу
        bot.register_next_step_handler(message, distribution)                                               #  Редирект в основную функцию (см. функцию distribution)

    elif(message.text==INFO_BAND_BUTTONS[1]):                                                           # Если пользователь хочет получить ссылки на концерты
        bot.send_message(message.chat.id, INFO_BAND_EVENTS_TEXT, 
                         reply_markup=keyboard(DISTRIBUTION_BUTTONS))                                       # Отправка сообщения с концертами
        bot.register_next_step_handler(message, distribution)                                               #  Редирект в основную функцию (см. функцию distribution)

    else:                                                                                               # Если пользователь не нажал на кнопку и ввел что то свое  
        bot.send_message(message.chat.id, PRESS_BUTTON_TEXT, 
                         reply_markup=keyboard(INFO_BAND_BUTTONS+DISTRIBUTION_BUTTONS))                     # Отправка сообщения с просьбой нажать на кнопку
        bot.register_next_step_handler(message, info_band)                                                  # Редирект в эту же функцию

#-------------------------------------------------------------------------------------------------- Обработка рассылки ----------------------------------------------------------------------------------------------------------------------------------------------   

def mailing(message):                                                                               # Создание функции mailing
    if(message.text==DISTRIBUTION_BUTTONS[0]):                                                          # Если пользователь нажал кнопку возврата в меню
        bot.send_message(message.chat.id, MAIN_TEXT, 
                         reply_markup=keyboard(MAIN_BUTTONS))                                               # Отправка приветствия с кнопками
        bot.register_next_step_handler(message, distribution)                                               # Редирект в основную функцию (см. функцию distribution)

    elif(message.text==MAILING_BUTTONS[0]):                                                             # Если пользователь хочет подписаться на рассылку
        bot.send_message(message.chat.id, MAILING_STАRT_TEXT, 
                         reply_markup=keyboard(DISTRIBUTION_BUTTONS))                                       # Отправка сообщения об успешной подписке
        mailing_users.append(str(message.chat.id))                                                          # Добавление пользователя в рассылку
        bot.register_next_step_handler(message, distribution)                                               # Редирект в основную функцию (см. функцию distribution)

    elif(message.text==MAILING_BUTTONS[1]):                                                             # Если пользователь хочет отписаться от рассылки
        bot.send_message(message.chat.id, MAILING_END_TEXT, 
                         reply_markup=keyboard(DISTRIBUTION_BUTTONS))                                       # Отправка сообщения об успешной отписке
        mailing_users.remove(str(message.chat.id))                                                          # Убираем пользователя из рассылку
        bot.register_next_step_handler(message, distribution)                                               # Редирект в основную функцию (см. функцию distribution)

    else:                                                                                               # Если пользователь не нажал на кнопку и ввел что то свое 
        if(str(message.chat.id) in mailing_users):                                                          # Если пользователь уже подписан на рассылку
            bot.send_message(message.chat.id, PRESS_BUTTON_TEXT, 
                             reply_markup=keyboard([MAILING_BUTTONS[1]]+DISTRIBUTION_BUTTONS))                  # Отправка информации о рассылке с кнопками отписки и базовой кнопки
        else:                                                                                               # Если пользователь еще не подписан на рассылку
            bot.send_message(message.chat.id, PRESS_BUTTON_TEXT, 
                             reply_markup=keyboard([MAILING_BUTTONS[0]]+DISTRIBUTION_BUTTONS))                  # Отправка информации о рассылке с кнопками подписки и базовой кнопки
        bot.register_next_step_handler(message, mailing)                                                    # Редирект в эту же функцию


#-------------------------------------------------------------------------------------------------- Обработка вопросов ----------------------------------------------------------------------------------------------------------------------------------------------   

def question(message):                                                                              # Создание функции question
    if(message.text==DISTRIBUTION_BUTTONS[0]):                                                          # Если пользователь нажал кнопку возврата в меню
        bot.send_message(message.chat.id, MAIN_TEXT, 
                         reply_markup=keyboard(MAIN_BUTTONS))                                               # Отправка приветствия с кнопками
    else:                                                                                               # Если пользователь ввел вопрос
        bot.send_message(message.chat.id, "Ответ на вопрос)", 
                         reply_markup=keyboard(DISTRIBUTION_BUTTONS))                                       # Отправка ответа на вопрос

    bot.register_next_step_handler(message, distribution)                                               # Редирект в основную функцию (см. функцию distribution)


@bot.message_handler(commands=["mailing_try"])
def test():
    global mailing_day
    mailing_day-=1 

@bot.message_handler(commands=["limit_try"])
def test():
    global fortune_telling_day
    fortune_telling_day-=1 

#-------------------------------------------------------------------------------------------------- Создание кнопок ----------------------------------------------------------------------------------------------------------------------------------------------   

def keyboard(button=[]):                                                                            # Создание функции keyboard
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)                                            # Создание маркапа
    for i in range(len(button)):                                                                        # Цикл проходящий по всем элементам массива button
        markup.add(types.KeyboardButton(button[i]))                                                         # Добавление кнопки
    return markup                                                                                       # Возвращение маркапа

#-------------------------------------------------------------------------------------------------- Рассылка ---------------------------------------------------------------------------------------------------------------------------------------------- 

def check_mail():                                                                                   # Создание функции check_mail
    global mailing_day                                                                                  # Получение доступа к переменной извне для дальнейшего изменения
    while True:                                                                                         # Цикл, который будет производиться всегда
        if(datetime.now().day!=mailing_day):                                                                # Если день, который помнит бот не совпадает с сегодняшним днем
            for id in mailing_users:                                                                            # Цикл идущий по всем айдишникам пользователей, подписанных на рассылку
                bot.send_message(id, gen_mailing_text)                                                              # Отправка сообщения с гороскопом (текст генерирует другая функция (см. функцию gen_mailing_text))      
            mailing_day=datetime.now().day                                                                      # Замена даты, которую помнит бот на сегодняшню

#-------------------------------------------------------------------------------------------------- Генирация текста рассылки ---------------------------------------------------------------------------------------------------------------------------------------------- 

def gen_mailing_text():
    return "рассылка"

#---------------------------------------------------------------------------------------------- Непрерывная работа ----------------------------------------------------------------------------------------------------------------------------------------------   

thread = threading.Thread(target=check_mail)                                                        # Создание потока который будет отвечать за рассылку
thread.start()                                                                                      # Запуск потока
bot.infinity_polling()                                                                              # Функция благодаря которой бот непрерывно работает