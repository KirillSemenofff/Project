import flask
import telebot

from functions import unix, send_zipfile

import os
import zipfile
import shutil
from multiprocessing.dummy import Pool

pool = Pool(20)
def executor(fu):
    def run(*a,**kw):
        pool.apply_async(fu, a, kw)
    return run

API_TOKEN=''
bot = telebot.TeleBot(API_TOKEN)
app = flask.Flask(__name__)

#200, Ok --пустая страница
@app.route('/', methods=['GET', 'HEAD'])
def index():
    return 'Unix'

#webhook
@app.route('/', methods=['POST'])
def webhook():
    if flask.request.headers.get('content-type') == 'application/json':
        json_string = flask.request.get_data().decode('utf-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return ''
    else:
        flask.abort(403)

#Начинаем работу с ботом, с помощью команды /start, и скидываем инстркуцию(если надо) по использыванию
@bot.message_handler(commands=['start'])
@executor
def start(message):
    bot.send_message(message.chat.id, text='Привет, отправь свое видео(не больше 20 MB), которое нужно уникализировать')

@bot.message_handler(content_types=['text'])
def func(message):
    if (message.text == '/unix'):
        send_message(message)
    elif (message.text == 'stop'):
        bot.send_message(message.chat.id, 'Ждем')

def send_message(message):
    x = bot.send_message(message.chat.id, 'отправьте мне zip-file')
    bot.register_next_step_handler(x, handle_docs)


# @bot.message_handler(content_types=['document'])
def handle_docs(message):
    try:
        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        try:
            os.chdir(r'C:\Users\79057\Desktop\betterunix\videos')                 #Переходим в папку videos
            os.mkdir('videos' + str(message.chat.id))                             #Создание новой папки, в которой будут сохраняться наше видео
            folder_name = ('videos' + str(message.chat.id))                       #Название папки состоит из "videos" и чата айди
        except FileExistsError as e:
            bot.reply_to(message, 'Такая папка уже существует')
        src_save_zip = rf'\{message.document.file_name}'                          #Путь для сохранения присланного нам zip-file
        src = f'{folder_name}'                                                                   #Папка для извлечения zip-file
        with open(src_save_zip, 'wb') as new_file:                                               #Сохранение zip-file
            new_file.write(downloaded_file)
        bot.reply_to(message, "Файл сохранен, идет уникализация видео, подождите...")
        archive = f'{message.document.file_name}'                                                #Сохраненный нами zip-file
        with zipfile.ZipFile(archive, 'r') as zip_file:
            zip_file.extractall(src)                                                             #Извлечение видео из zip-file пользователя
        unix(folder_name)                                                                        #Вызоваем функцию, которая унифицирует видео
        os.remove(rf'C:\Users\79057\Desktop\betterunix\videos\{message.document.file_name}')   #Удаляем присланный нам от пользователя zip-file
        send_zipfile(message, folder_name, bot)                                      #Вызываем функцию, которая отправляет архив с готовым видео
        shutil.rmtree(rf'C:\Users\79057\Desktop\betterunix\videos\{folder_name}')              #Удаляем папку с видео
    except Exception as e:
        bot.reply_to(message, e)


if __name__ == '__main__':
    app.run(debug=True)

