import telebot
import camera
import time
import timedelta
from time import sleep
import foto
from threading import *
import readconfig as rc
from os_info import OsInfo
from simple_logging import Logging, PrintToFile, PrintToConsole, LogRotate


bot = telebot.TeleBot(rc.config_dict['TOKEN'])

logging = Logging(rc.log_file_dir)
logrotate = LogRotate(rc.log_file_dir)

move_foto = foto.FotoMove(rc.image_schedule_dir, rc.image_user_dir)
foto_zip_user = foto.FotoZip(rc.image_user_dir, rc.image_user_arch_dir)
foto_zip_schedule = foto.FotoZip(rc.image_schedule_dir, rc.image_schedule_arch_dir)

os_time = OsInfo()
check_rotate = timedelta.CheckRotate()


for key, value in rc.camera_id.items():
    logging.log(f'Старт бота с камерами {key}, {value}', PrintToFile, PrintToConsole)


@bot.message_handler(commands=['start'])
def send_welcome(message):
    counter = 0
    for key, value in rc.admin_id.items():
        if value == message.chat.id:
            bot.send_message(value, 'Бот запущен и полностью функционирует')
            logging.log(f'Сообщение отправлено пользователю {key} с ID:{value}', PrintToFile)
            break
        counter += 1

        if len(rc.admin_id) == counter:
            logging.log(f'Попытка получить данные от незарегистрированного пользователя {message.chat.id}', PrintToFile, PrintToConsole)


@bot.message_handler(commands=['foto'])
def send_foto(message):
    counter = 0
    for key, value in rc.admin_id.items():
        if value == message.chat.id:
            bot.reply_to(message, 'Одну минуту, фото сейчас отправится')
            for number, cam in rc.camera_id.items():
                camera.screen_shot(number, cam)
                bot.send_photo(message.chat.id, open(f'cam{number}.jpg', 'rb'), caption=f'{os_time.get_time()} Camera number {number}')
                move_foto.user_foto(number)
                logging.log(f'Фото отправлено пользователю {key} ID: {value} on Camera number {number}', PrintToFile, PrintToConsole)
            break
        counter += 1

        if len(rc.admin_id) == counter:
            logging.log(f'Попытка получить фото от незарегистрированно пользователя ID:{message.chat.id}', PrintToFile, PrintToConsole)


def send_schedule_message(minutes, camera_number):
    for number, cam in rc.camera_id.items():
        camera.screen_shot(number, cam)
        bot.send_photo(rc.chat_id,
                       open(f'cam{camera_number}.jpg', 'rb'),
                       caption=(os_time.get_time() + f' Отправка каждые {minutes}'
                                                     f' минут с камеры {camera_number}'), timeout=100)
        move_foto.schedule_foto(camera_number)
        logging.log(f'Отправка фотоа раз в {minutes} минут', PrintToConsole, PrintToFile)


def rotate_file():
    while True:
        if os_time.time_format() == '00:00':
            print('Время для проверки архивов')
            if check_rotate.check_logfile(rc.log_file_dir, rc.log_file_period):
                print('Запуск архивации лог файла')
                logrotate.zip()
            if check_rotate.check_foto(rc.image_schedule_dir, rc.image_archive_period):
                print('Запуск архивации schedule_foto')
                foto_zip_schedule.foto_zip()
            if check_rotate.check_foto(rc.image_user_dir, rc.image_archive_period):
                print('Запуск архивации user_foto')
                foto_zip_user.foto_zip()
            time.sleep(65)
        time.sleep(10)


def send_message_timer():
    while True:
        time.sleep(2)
        if os_time.time_format() in rc.send_time:
            logging.log(f'Время совпадает с {os_time.time_format()} начинаем отправку фото', PrintToFile, PrintToConsole)
            for c in rc.camera_id:
                send_schedule_message(rc.interval, c)
            time.sleep(65)


schedule_timer_job = Thread(target=send_message_timer, daemon=True, name='schedule_timer')
schedule_timer_job.start()

rotate_file_job = Thread(target=rotate_file, daemon=True, name='rotate_file')
rotate_file_job.start()

if __name__ == '__main__':
    while True:
        try:
            bot.polling(none_stop=True)
        except Exception as e:
            logging.log(f'{e}', PrintToFile)
            sleep(15)
