import telebot
from telebot import types
from conf import TOKEN
import time
from collections import defaultdict

bot = telebot.TeleBot(TOKEN)

user_last_search_time = defaultdict(float)
search_interval = 20  # Минимальный интервал между запросами (в секундах)

#команды
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! \nЯ Solution — твой помощник в решении задач.  Я могу помочь тебе найти информацию, ответить на вопросы и многое другое.  Для начала работы, попробуй использовать команду /search, чтобы найти то, что тебя интересует, или /help, чтобы узнать о моих возможностях.', reply_markup=klav)
    bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAALqfGdKZmxMSKp00lnqfTwtoHV6_QABgQAC4kwAAvJGQUsvrXW_b9GBjDYE')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, f'Я Solution, и я здесь, чтобы помочь! \n\nВот список команд, которые я понимаю: \n/start:  Начать работу со мной. \n/search:  Найти информацию по вашему запросу. \n/help:  Показать это сообщение о помощи. \n\nЕсли у тебя есть другие вопросы, пожалуйста, задай их!')

@bot.message_handler(content_types=['photo','audio', 'video','voice'])
def help(message):
    bot.send_message(message.chat.id, f'Я могу обрабатывать только текстовые сообщения')

@bot.message_handler(commands=['search'])
def search(message):
    user_id = message.chat.id
    current_time = time.time()

    # Проверка, прошло ли достаточно времени с последнего запроса на /search
    if current_time - user_last_search_time[user_id] < search_interval:
        bot.send_message(message.chat.id, "Пожалуйста, подождите 20 секунд перед новым запросом.")
        return  # Прерываем выполнение функции, чтобы не обрабатывать запрос

    # Обновляем время последнего запроса на /search
    user_last_search_time[user_id] = current_time

    bot.send_message(message.chat.id, f'Пожалуйста, введи поисковый запрос. Например: "Код для игры змейка на пайтоне".  Чем точнее твой запрос, тем лучше результаты.')
    bot.register_next_step_handler(message, process_search)
    
@bot.message_handler(content_types=['text'])
def talking(message):
    user_id = message.chat.id
    current_time = time.time()
    if message.text == "Помощь":
        bot.send_message(message.chat.id, f'Я Solution, и я здесь, чтобы помочь! \n\nВот список команд, которые я понимаю: \n/start:  Начать работу со мной. \n/search:  Найти информацию по вашему запросу. \n/help:  Показать это сообщение о помощи. \n\nЕсли у тебя есть другие вопросы, пожалуйста, задай их!')
    elif message.text == "Поиск":

        # Проверка, прошло ли достаточно времени с последнего запроса на "Поиск"
        if current_time - user_last_search_time[user_id] < search_interval:
            bot.send_message(message.chat.id, "Пожалуйста, подождите 20 секунд перед новым запросом.")
            return  # Прерываем выполнение функции, чтобы не обрабатывать запрос
        user_last_search_time[user_id] = current_time

        bot.send_message(message.chat.id, f'Пожалуйста, введи поисковый запрос. Например: "Код для игры змейка на пайтоне".  Чем точнее твой запрос, тем лучше результаты.')
        bot.register_next_step_handler(message, process_search)
    elif message.text == "По дате":
        bot.send_message(message.chat.id, f'Участок кода фильтра "по дате"')
    elif message.text == "По рейтингу":
        bot.send_message(message.chat.id, f'Участок кода фильтра "по рейтингу"')
    elif message.text == "По релевантности":
        bot.send_message(message.chat.id, f'Участок кода фильтра "по релевантности"')
    else:
        bot.send_message(message.chat.id, f'Извини, я тебя не понимаю')

#важная часть
#функция с сохранением переменной
def process_search(message):
    request = message.text  # Сохраняем строковое значение

    bot.send_message(message.chat.id, f'Ты искал: {request}')
    
    
    bot.send_message(message.chat.id, f'Нажми на кнопку для выбора фильтра', reply_markup=search_button)



#клавиутара

klav = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button1 = types.KeyboardButton("Помощь")   
button2 = types.KeyboardButton("Поиск")
klav.add(button1,button2)

search_button = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
button4 = types.KeyboardButton("По дате")
button5 = types.KeyboardButton("По рейтингу")
button6 = types.KeyboardButton("По релевантности")
search_button.add(button4,button5, button6)

bot.polling(non_stop=True)
