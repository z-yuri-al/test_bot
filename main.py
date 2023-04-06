import telebot
import webbrowser
import requests
import json
#создаем бота, указываю токен, полученный при регистрации
api = ''
bot = telebot.TeleBot(api)
api_weather = 'd230b11a87048e77a21dcc7e82527a69'

#обрабатываем полученные команды
@bot.message_handler(commands=['help', 'привет'])
# @bot.message_handler(textwrap =['hello', 'hi', 'привет'])

def hello(messange):
    if messange.from_user.last_name == None: #проверяем есть ли фамилия у пользователя
        hello_messange = f'Привет <b>{messange.from_user.first_name}</b>' #создаем приветственное сообщение
    else:
        hello_messange = f'Привет <b>{messange.from_user.first_name} <u>{messange.from_user.last_name}</u></b>'
    bot.send_message(messange.chat.id, hello_messange, parse_mode='html') #отправляем сообщение
    # bot.send_message(messange.chat.id, messange.from_user, parse_mode='html')

# @bot.message_handler(commands=['start'])
# def start(message):
#     markup = telebot.types.ReplyKeyboardMarkup()
#     btn_1 = telebot.types.KeyboardButton('Перейти на сайт')
#     markup.row(btn_1)
#     btn_2 = telebot.types.KeyboardButton('удалить')
#     btn_3 = telebot.types.KeyboardButton('изменить текст')
#     markup.row(btn_2, btn_3)
#     stic = open('sticker.webp', 'rb')
#     bot.send_sticker(message.chat.id, stic)
#     bot.send_message(message.chat.id, f'Привет 👋 <b>{message.from_user.first_name}</b>', reply_markup=markup, parse_mode='html')
#     bot.register_next_step_handler(message, on_click) #следущий шаг выполнения программы переводит на функцию on_click
#
# def on_click(message): #создаем эту функцию
#     if message.text == 'Перейти на сайт':
#         webbrowser.open('https://tzfilm.ru')
#         bot.send_message(message.chat.id, 'Сайт открыт')
#     elif message.text == 'удалить':
#         bot.send_message(message.chat.id, 'сообщение удалено')
#     # bot.register_next_step_handler(message, on_click) # зацикливает функцию

price = None
first_payment = None
year = None
percent = None

def calculator(price_f, first_payment_f, year_f, percent_f):
    summ = price_f - first_payment_f
    month_percent = percent_f / 12 / 100
    # month_payment = (summ * month_percent) / (1 - ((1 + month_percent) * (1 - year_f * 12)))
    month_payment = summ * month_percent * ((1 + month_percent) ** (year_f * 12)) / (((1 + month_percent) ** (year_f * 12)) - 1)
    return round(month_payment, 2)

@bot.message_handler(commands=['start'])
def start(message):
    stic = open('sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, stic)
    bot.send_message(message.chat.id, f'Привет <b>{message.from_user.first_name}</b>. Я помогу тебе расчитать ежемесячный платеж по ипотеке', parse_mode='html')
    bot.send_message(message.chat.id, 'Введите стоимость квартиры:')
    bot.register_next_step_handler(message, get_price)

def get_price(message):
    global price
    price = int(message.text)
    bot.send_message(message.chat.id, 'Введите сумму первоначального взноса:')
    bot.register_next_step_handler(message, get_first_payment)

def get_first_payment(message):
    global first_payment
    first_payment = int(message.text)
    bot.send_message(message.chat.id, 'На сколько лет Вы хотите взять ипотеку?')
    bot.register_next_step_handler(message, get_year)

def get_year(message):
    global year
    year = int(message.text)
    bot.send_message(message.chat.id, 'Какая процентная ставка по кредиту?')
    bot.register_next_step_handler(message, get_percent)

def get_percent(message):
    global percent
    percent = int(message.text)
    bot.send_message(message.chat.id, 'Подождите секунду, сейчас посчитаю)')
    # bot.register_next_step_handler(message, payment)
    payment = calculator(price, first_payment, year, percent)
    bot.send_message(message.chat.id, f'Ваш ежемесячный плажет по ипотеке составит <b>{payment}</b> рублей', parse_mode='html')


# def payment(message):
#     payment = calculator(price, first_payment, year, percent)
#     bot.send_message(message.chat.id, f'Ваш ежемесячный плажет по ипотеке составит <b>{payment}</b> рублей', parse_mode='html')


@bot.message_handler(commands=['weather', 'погода'])
def weather(message):
    bot.send_message(message.chat.id, f'Привет <b>{message.from_user.first_name}</b>. Я помогу тебе узнать погоду, введите название города', parse_mode='html')
    bot.register_next_step_handler(message, get_weather)

def get_weather(message):
    city = message.text.strip().lower()
    result = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_weather}&units=metric') #request нужен чтобы получить результат с сайта или отправить данные на сервер
    #параметр берем с сайта в разделе api
    temp = json.loads(result.text) #преобразуем json информацию в обчный для питона вид (словарь)
    bot.reply_to(message, f'Температура воздуха сейчас {temp["main"]["temp"]} °C')






# @bot.message_handler(commands=['site', 'website', 'сайт', 'вебсайт'])
# def site(message):
#     webbrowser.open('https://tzfilm.ru')
#
# @bot.message_handler(content_types=['photo']) #обрабатываем фото
# def get_photo(message):
#     markup = telebot.types.InlineKeyboardMarkup() #создаем markup чтобы потом добавлять туда кнопки
#     btn_1 = telebot.types.InlineKeyboardButton('Перейти на сайте', url='https://tzfilm.ru') #создаем кнопки
#     markup.row(btn_1) #добавляем кпопки по рядам
#     btn_2 = telebot.types.InlineKeyboardButton('удалить фото', callback_data='delete')
#     btn_3 = telebot.types.InlineKeyboardButton('изменить текст', callback_data='edit')
#     markup.row(btn_2, btn_3)
#     bot.reply_to(message, 'какое красивое фото', reply_markup = markup) #выводим сообщение с кнопкой
#
#
# @bot.callback_query_handler(func=lambda callback: True) #создаем функции для callback_data
# def callback_message(callback):
#     if callback.data == 'delete':
#         bot.delete_message(callback.message.chat.id, callback.message.message_id - 1)
#     if callback.data == 'edit':
#         bot.edit_message_text('измененный текст', callback.message.chat.id, callback.message.message_id )
#
#
# #обрабатываем введенные сообщения
# @bot.message_handler()
# def get_user_text(message):
#     if message.text.lower() == 'привет':
#         bot.send_message(message.chat.id, f'И тебе привет!')
#     elif message.text.lower() == 'id':
#         bot.reply_to(message, f'ID: {message.from_user.id}')
#     elif message.text.lower() == 'photo':
#         photo = open('image.jpeg', 'rb')
#         bot.send_photo(message.chat.id, photo)
#     elif message.text.lower() == 'music':
#         misic = open('bi-2-lajjki.mp3', 'rb')
#         bot.send_audio(message.chat.id, misic)
#     elif message.text.lower() == 'video':
#         video = open('P1004561.MOV', 'rb')
#         bot.send_video(message.chat.id, video)
#     else:
#         bot.send_message(message.chat.id, '<u>Я Вас не понял</u>', parse_mode='html')

# def request_page(message):
#     send = bot.send_message(message.chat.id, 'Введите данные')
#     bot.register_next_step_handler(send, verify_page)
#
#
# def verify_page(message):
#     price, first_payment, year, percent = int(message.text.isdigit()), int(message.text.isdigit()), int(message.text.isdigit()), int(message.text.isdigit())# проверяем что введённое сообщение от пользователя является цифрой
#     print(calculator(price, first_payment, year, percent))




bot.polling(none_stop= True) #постоянно проверяет новые сообщения от пользователя
