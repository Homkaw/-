import telebot

from telebot import types
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from time import sleep
from selenium.webdriver.common.by import By
from database import Database

bot = telebot.TeleBot(TOKEN)

user_last_search_time = defaultdict(float)
search_interval = 20  # Минимальный интервал между запросами (в секундах)
count_post = 5

service = Service(executable_path=ChromeDriverManager().install())
driver = webdriver.Chrome(service=service)
db = Database('bot_db.db')
filter = "По релевантности" # Выбираем фильтр

#команды
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}! \nЯ Solution — твой помощник в решении задач.  Я могу помочь тебе найти информацию, ответить на вопросы и многое другое.  Для начала работы, попробуй использовать команду /search, чтобы найти то, что тебя интересует, или /help, чтобы узнать о моих возможностях.', reply_markup=klav)
    if db.add_user(callback.from_user.id):
        callback.answer("Вы успешно добавлены в базу данных!")
    else:
        callback.answer("Ошибка при добавлении в базу данных. Попробуйте позже.")

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
        bot.send_message(message.chat.id, f'Фильтр установлен по дате')
        filter = "По дате"
    elif message.text == "Парсинг на python":
        bot.send_message(message.chat.id, f'Запущен поиск данных...')
        find = "Парсинг на python"
        urlpath= f'https://habr.com/ru/search/?q={find}&target_type=posts&order=relevance'
        driver.get(urlpath)
        tpa = []
        def filter_set():
            if filter == "По релевантности":
                filter_change = driver.find_element("xpath", '//*[text()="по релевантности "]')
                filter_change.click()
            elif filter == "По времени":
                filter_change = driver.find_element("xpath", '//*[text()="по времени "]')
                filter_change.click()
            elif filter == "По рейтингу":
                filter_change = driver.find_element("xpath", '//*[text()="по рейтингу "]')
                filter_change.click()
            else:
                print("Такого фильтра нет")
            sleep(5)
    elif message.text == "По рейтингу":
        bot.send_message(message.chat.id, f'Фильтр установлен по рейтингу')
        filter = "По рейтингу"
    elif message.text == "По релевантности":
        bot.send_message(message.chat.id, f'Фильтр установлен по релевантности')
        filter = "По релевантности"

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
