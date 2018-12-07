import telebot
import constants
import requests
import urllib.request, json
from collections import Counter
from pydub import AudioSegment
from ffmpy import FFmpeg

bot = telebot.TeleBot(constants.token)
urlvoice = "https://api.telegram.org/bot534897366:AAGLaU_kh5Ae8RE_Ww7cJ7nH97x8-nL8I1c/getUpdates"
url1 = "https://m81kko67a8.execute-api.us-east-1.amazonaws.com/v0/rahmet-api"

API_ENDPOINT = 'https://api.wit.ai/speech'
ulat = 0
ulng = 0




@bot.message_handler(commands=['start'])
def handle_start(message):
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
    user_markup.row("Поиск Банков")
    bot.send_message(message.chat.id, 'Добро пожаловать!', reply_markup=user_markup)
    print(message.chat.id)

@bot.message_handler(content_types=['text'])
def handle_text(message):
    global time, address
    user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

    def know_order():
        data = {"procedure": "know_order", "sender_id": message.chat.id, "bank_id": 1, "time": time}
        r = requests.post(url1, json=data)
        text = r.content.decode('utf8').replace("'", '"')
        s = json.loads(text)
        if s == "error":
            print("fghj")
            bot.send_message(message.chat.id, 'Ваша очередь прошла', reply_markup=user_markup)
            return None
        else:
            left = s.get('left')
            print(left)
            print(s)
            print(r.json)
            print(data)
            bot.send_message(message.chat.id, 'Перед Вами ' + str(left) + ' человек', reply_markup=user_markup)
            return left

    def take_order():
        time = 5
        print("fghjk")
        data = {'procedure': 'take_order', 'time': 5, 'bank_id': 1, 'sender_id': message.chat.id}
        r = requests.post(url1, json=data)
        text = r.content.decode('utf8').replace("'", '"')
        s = json.loads(text)

        if s != "error":
            print("fghjk")
            left = s.get('left')
            print("#######")
            print(text)
            print(s)
            print(data)
            print(left)
            user_markup.row("Узнать очередь")
            user_markup.row("Назад")
            bot.send_message(message.chat.id, 'Вы успешно зарегистрировались!', reply_markup=user_markup)

            if left == 1:
                bot.send_message(message.chat.id, "Вам осталось 10 минут ожидания\n Перед вами "+ str(left) +" человек", disable_notification=False)
            elif left == 2:
                bot.send_message(message.chat.id, "Вам осталось 25 минут ожидания\n Перед вами "+ str(left) +" человек", disable_notification=False)

        else:
            print("error")
            bot.send_message(message.chat.id, 'Вы уже стоите в очереди!', reply_markup=user_markup)

    if message.text == "Поиск Банков":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button = telebot.types.KeyboardButton(text="Ближайшие", request_location=True)
        listed = telebot.types.KeyboardButton(text="В городе")
        back = telebot.types.KeyboardButton(text="Назад")
        keyboard.add(button, listed, back)

        bot.send_message(message.chat.id, "Выберите ", reply_markup=keyboard)

    elif message.text == "Ближайшие":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button = telebot.types.KeyboardButton(text="📍 Отправить местоположение", request_location=True)
        back = telebot.types.KeyboardButton(text="Назад")
        keyboard.add(button, back)
        bot.send_message(message.chat.id, "Отправьте, пожалуйста, локацию: ", reply_markup=keyboard)

    elif message.text == "В городе":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        button = telebot.types.KeyboardButton(text="📍 Отправить местоположение", request_location=True)
        back = telebot.types.KeyboardButton(text="Назад")
        keyboard.add(button, back)
        bot.send_message(message.chat.id, "Отправьте, пожалуйста, локацию: ", reply_markup=keyboard)

    if message.text == "Занять очередь":
        keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
        card = telebot.types.KeyboardButton(text="Создать карточку")
        credit = telebot.types.KeyboardButton(text="Получить кредит")
        balance = telebot.types.KeyboardButton(text="Пополнить счет")
        back = telebot.types.KeyboardButton(text="Назад")
        keyboard.add(card, credit, balance, back)
        bot.send_message(message.chat.id, "Выберите операцию", reply_markup=keyboard)
    elif message.text == "Создать карточку":
        time = 15
        take_order()
    elif message.text == "Получить кредит":
        time = 30
        take_order()
    elif message.text == "Пополнить счет":
        time = 5
        take_order()
    elif message.text == "Узнать очередь":
        know_order()
    elif message.text == "Назад":
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
        user_markup.row("Поиск Банков")
        user_markup.row("Занять очередь")
        bot.send_message(message.chat.id, 'Меню', reply_markup=user_markup)

@bot.message_handler(content_types=['location'])
def handle_location(message):
    global ulat, ulng
    ulat = str(message.location.latitude)
    ulng = str(message.location.longitude)
    path = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=bank&location=" + str(ulat) + "," + str(ulng) + "&radius=300&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI"
    with urllib.request.urlopen(path) as url:
        data = json.loads(url.read().decode())['results']
        for i in range(len(data)):
            lat = data[i]['geometry']['location']['lat']
            lng = data[i]['geometry']['location']['lng']
            name = data[i]['name']
            address = data[i]['formatted_address']
            if ('opening_hours' in data[i]):
                openow = data[i]['opening_hours']['open_now']
                opennow = ""
                if (openow == True):
                    opennow = "Open"
                elif (openow == False):
                    opennow = "Close"
            else:
                opennow = "unknown"
            if ('rating' in data[i]):
                rating = data[i]['rating']
            else:
                rating = "unknown"

            if not (name.lower().find("halyk") == -1):
                bot.send_message(message.chat.id, "📌 name: " + str(name) + "\n" + "📍 address: " + str(
                    address) + "\n" + "⭐️ rating: " + str(
                    rating) + "\n" + "🚪 Open/Close: " + opennow + "\n" + "📍 location: ")
                bot.send_location(message.chat.id, lat, lng)
                keyboard = telebot.types.InlineKeyboardMarkup()
                button = telebot.types.InlineKeyboardButton(text="Выбрать", callback_data='test1')
                keyboard.add(button)
                bot.send_message(message.chat.id, 'Нажмите на кнопку', reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    global ulat, ulng
    path = "https://maps.googleapis.com/maps/api/place/textsearch/json?query=bank&location=" + str(ulat) + "," + str(ulng) + "&radius=300&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI"
    with urllib.request.urlopen(path) as url:
        data = json.loads(url.read().decode())['results']
        for i in range(len(data)):
            if call.data == "test" + str(i):
                name = data[i]['name']
                address = data[i]['formatted_address']
                print(address)
                return address
            bot.answer_callback_query(callback_query_id=call.id, show_alert=False, text="Добавлено!")

def read_audio(WAVE_FILENAME):
    with open(WAVE_FILENAME, 'rb') as f:
        audio = f.read()
    return audio

@bot.message_handler(content_types=["voice"])
def handle_voice(message):
    data = requests.get(urlvoice, None)
    if data:
        data = data.text
        json_data = json.loads(data)

    if not json_data['result']:
        bot.send_message(message.from_user.id, 'Попробуйте еще раз')

    else:
        bot.send_message(message.from_user.id, 'Подождите чуть-чуть...')
        file_idwka = json_data['result'][0]['message']['voice']['file_id']
        file_path_urlq = 'https://api.telegram.org/bot534897366:AAGLaU_kh5Ae8RE_Ww7cJ7nH97x8-nL8I1c/getFile?file_id=' + file_idwka
        data1 = requests.get(file_path_urlq).text
        json_data1 = json.loads(data1)
        file_pathwka = json_data1['result']['file_path']

        print("downloading")
        url_file = 'https://api.telegram.org/file/bot534897366:AAGLaU_kh5Ae8RE_Ww7cJ7nH97x8-nL8I1c/' + file_pathwka
        requests.get(url_file)
        g = requests.get(url_file, stream=True)
        voice_filename = "voice.mp3"
        with open(voice_filename, "wb") as o:
            o.write(g.content)

        AudioSegment.from_file(voice_filename, "ogg").export(voice_filename, format="mp3")
        audio = read_audio(voice_filename)

        headers = {'authorization': 'Bearer ' + 'C6RBEQMC3A7BCNCN4BSJCCLNYGMVFL2F', 'Content-Type': 'audio/mpeg3'}
        resp = requests.post(API_ENDPOINT, headers=headers, data=audio)
        respon = json.loads(resp.content)
        user_output = respon['_text'].lower()
        #bot.send_message(message.from_user.id, user_output)
        user_words = user_output.split()
        for item in range(0, int(len(user_words))):
            user_words[item] = user_words[item].lower()
        global time, address
        user_markup = telebot.types.ReplyKeyboardMarkup(True, False)

        def know_order():
            data = {"procedure": "know_order", "sender_id": message.chat.id, "bank_id": 1, "time": time}
            r = requests.post(url1, json=data)
            text = r.content.decode('utf8').replace("'", '"')
            s = json.loads(text)
            if s == "error":
                bot.send_message(message.chat.id, 'Ваша очередь прошла', reply_markup=user_markup)
                return None
            else:
                left = s.get('left')
                print(left)
                print(s)
                print(r.json)
                print(data)
                bot.send_message(message.chat.id, 'Перед вами ' + str(left) + ' человек', reply_markup=user_markup)
                return left

        def take_order():
            data = {'procedure': 'take_order', 'time': time, 'bank_id': 1, 'sender_id': message.chat.id}
            r = requests.post(url1, json=data)
            text = r.content.decode('utf8').replace("'", '"')
            s = json.loads(text)
            if s != "error":
                left = s.get('left')
                print("#######")
                print(text)
                print(s)
                print(r.json)
                print(data)
                print(left)
                user_markup.row("Узнать очередь")
                user_markup.row("Назад")
                bot.send_message(message.chat.id, 'Вы успешно зарегистрировались!', reply_markup=user_markup)
                if left == 1:
                    bot.send_message(message.chat.id,
                                     "Вам осталось 10 минут ожидания\n Перед вами " + str(left) + " человек",
                                     disable_notification=False)
                elif left == 2:
                    bot.send_message(message.chat.id,
                                     "Вам осталось 25 минут ожидания\n Перед вами " + str(left) + " человек",
                                     disable_notification=False)
            else:
                print("error")
                bot.send_message(message.chat.id, 'Вы уже стоите в очереди!', reply_markup=user_markup)

        if not(user_output.find("банк")==-1):
            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button = telebot.types.KeyboardButton(text="Ближайшие", request_location=True)
            listed = telebot.types.KeyboardButton(text="В городе")
            back = telebot.types.KeyboardButton(text="Назад")
            keyboard.add(button, listed, back)

            bot.send_message(message.chat.id, "Выберите ", reply_markup=keyboard)

        elif not(user_output.find("ближайшие")==-1) or not(user_output.find("рядом")==-1):
            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            button = telebot.types.KeyboardButton(text="📍 Отправить местоположение", request_location=True)
            back = telebot.types.KeyboardButton(text="Назад")
            keyboard.add(button, back)
            bot.send_message(message.chat.id, "Отправьте, пожалуйста, локацию: ", reply_markup=keyboard)

        elif not(user_output.find("город")==-1):
            with urllib.request.urlopen(
                    "https://maps.googleapis.com/maps/api/place/textsearch/json?query=bank+in+Almaty&key=AIzaSyC0AuanxSq5DMmcnojnInlFRzqz0KF5HZI") as url:
                data = json.loads(url.read().decode())['results']
                for i in range(len(data)):
                    lat = data[i]['geometry']['location']['lat']
                    lng = data[i]['geometry']['location']['lng']
                    name = data[i]['name']
                    address = data[i]['formatted_address']
                    if ('opening_hours' in data[i]):
                        openow = data[i]['opening_hours']['open_now']
                        opennow = ""
                        if (openow == True):
                            opennow = "Open"
                        elif (openow == False):
                            opennow = "Close"
                    else:
                        opennow = "unknown"
                    if ('rating' in data[i]):
                        rating = data[i]['rating']
                    else:
                        rating = "unknown"
                    if not (name.lower().find("halyk") == -1):
                        bot.send_message(message.chat.id, "📌 name: " + str(name) + "\n" + "📍 address: " + str(
                            address) + "\n" + "⭐️ rating: " + str(
                            rating) + "\n" + "🚪 Open/Close: " + opennow + "\n" + "📍 location: ")
                        bot.send_location(message.chat.id, lat, lng)
                        keyboard = telebot.types.InlineKeyboardMarkup()
                        button = telebot.types.InlineKeyboardButton(text="Выбрать", callback_data="test1")
                        keyboard.add(button)
                        bot.send_message(message.chat.id, 'Нажмите на кнопку', reply_markup=keyboard)

        if not(user_output.find("занять очередь")==-1):
            keyboard = telebot.types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
            card = telebot.types.KeyboardButton(text="Создать карточку")
            credit = telebot.types.KeyboardButton(text="Получить кредит")
            balance = telebot.types.KeyboardButton(text="Пополнить счет")
            back = telebot.types.KeyboardButton(text="Назад")
            keyboard.add(card, credit, balance, back)
            bot.send_message(message.chat.id, "Выберите операцию", reply_markup=keyboard)
        elif not(user_output.find("карт")==-1):
            time = 15
            take_order()
        elif not(user_output.find("кредит")==-1):
            time = 30
            take_order()
        elif not(user_output.find("счет")==-1):
            time = 5
            take_order()
        elif not(user_output.find("узнать очередь")==-1):
            know_order()
        elif user_output == "назад":
            user_markup = telebot.types.ReplyKeyboardMarkup(True, False)
            user_markup.row("Поиск Банков")
            user_markup.row("Занять очередь")
            bot.send_message(message.chat.id, 'Меню', reply_markup=user_markup)

bot.polling(none_stop=True, interval=1)
