from simple_logging import Logging, PrintToConsole, PrintToFile
from os_info import OsInfo
import os

config_dict = {}
log_file_dir = []
log_level = 1
chat_id = []
admin_id = {}
camera_id = {}
send_time = []
interval = 10
log_file_period = 1
image_archive_period = 1
image_user_dir = []
image_user_arch_dir = []
image_schedule_dir = []
image_schedule_arch_dir = []

config_state = True

os_info = OsInfo()


try:
    with open('config.ini', 'r', encoding='UTF-8') as config_file:
        for line in config_file:
            if line[:1] != '#' and line[:1] != '\n':
                try:
                    key, value = [word.strip() for word in line.split('=')]
                    if value != '':
                        config_dict[key] = value
                    else:
                        print(f'Value in {key} is empty')
                        break
                except ValueError:
                    print(f'Value Error: expected 2, got 1. Check "config.ini", key {line.rstrip()} is empty')
                    break
except FileNotFoundError:
    print('Файл конфигурации config.ini не найден')

except PermissionError:
    print('Файл не может быть прочитан, проверьте права файла на чтение')

#  Проверка пути лог файла
if config_dict.get('LOG_FILE_DIR', False):
    log_file_dir = config_dict['LOG_FILE_DIR'].strip("'")
    try:
        try:
            with open(f'{log_file_dir}{os_info.slash}log.txt', 'a+', encoding='UTF8') as temp_log_file:
                temp_log_file.write(f'{os_info.get_time()}__________запись лога_______\n')
        except FileNotFoundError:
            print(f'Каталог {log_file_dir}{os_info.slash} не найден')
    except PermissionError:
        print(f'Ошибка доступа. в каталоге {log_file_dir} не удается создать файл log.txt')
else:
    print('Логфайл не может быть создан, проверьте путь')
    config_state = False

#   Установка уровня логирования
if config_dict.get('LOG_LEVEL', False):
    log_level = config_dict['LOG_LEVEL']
    print(f'Установка уровня логирования {config_dict["LOG_LEVEL"]}')
else:
    print('Используется уровень логирования по умолчанию')


logging = Logging(log_file_dir)
logging.log(f'Установка каталога для лог файла {log_file_dir}', PrintToFile)


#  Проверка токена
if config_dict.get('TOKEN', False):
    logging.log('Установка токена бота => OK', PrintToFile)
else:
    logging.log('Ошибка! Нет токена бота, добавьте в config.ini строку "TOKEN = your_token_bot"', PrintToFile)
    config_state = False

#  Создание списка чата(ов) куда отправлять фото по таймеру
if config_dict.get('CHAT_ID', False):
    temp_string = config_dict['CHAT_ID'].split(',')
    for item in temp_string:
        try:
            int(item)
        except ValueError:
            logging.log(f'В id чата "{item.strip()}" находится не число', PrintToFile)
            config_state = False
            break

        chat_id.append(int(item.strip()))

    logging.log(f'Список чатов для отправки фото по временным интервалам: {chat_id}', PrintToFile)
    logging.log('Установка CHAT_ID => OK', PrintToFile)

else:
    logging.log('Ошибка! Нет обязательного пункта, добавьте в config.ini строку "CHAT_ID = your_chat_id"', PrintToFile)
    config_state = False


#  Создание списка админов бота
for key in config_dict.keys():
    if key[:5] == 'ADMIN':
        admin = config_dict[key].split(':')
        try:
            admin_id[admin[0].strip()] = int(admin[1].strip())
        except ValueError:
            logging.log(f'В id чата "{admin[1].strip()}" находится не число', PrintToFile)
            config_state = False
            break

if len(admin_id) != 0:
    logging.log(f'Список администраторов бота: {admin_id}', PrintToFile)
    logging.log('Установка админа чата => OK', PrintToFile)
else:
    logging.log('Ошибка! Список администраторов пуст, добавьте хотя бы одного', PrintToFile)
    config_state = False

#  Создание списка камер
try:
    for key in config_dict.keys():
        if key[:1] in '0123456789':
            camera_id[int(key)] = config_dict[key]
    if len(camera_id) == 0:
        config_state = False
        raise ValueError
    else:
        logging.log(f'Список камер: {camera_id}', PrintToFile)
        logging.log('Установка камер => OK', PrintToFile)
except ValueError:
    logging.log('Ошибка! Список камер пуст, добавьте хотя бы одну камеру', PrintToConsole)

#  Получение интервала для отправки фото
if config_dict.get('TIME_SEND_INTERVAL', False):
    interval = int(config_dict['TIME_SEND_INTERVAL'].strip('m'))
    logging.log(f'Установка интервала {interval} минут => OK', PrintToFile)
else:
    logging.log(f'Интервал не задан, используется интервал по умолчанию - {interval}', PrintToFile)

#  Создание списка временного интервала отправки фото
if config_dict.get('TIME_SEND', False):
    try:
        data_split = config_dict['TIME_SEND'].split('-')
        start = data_split[0].strip()
        stop = data_split[1].strip()

        minutes_start = int(start[3:])
        hours_start = int(start[:2])

        minutes_stop = int(stop[3:])
        hours_stop = int(stop[:2])

        while True:
            if minutes_start > 59:
                hours_start += 1
                minutes_start = abs(minutes_start - 60)

            if hours_start > 23:
                hours_start = 0

            if hours_start == hours_stop:
                if minutes_stop == minutes_start:
                    send_time.append(f'{hours_start:02}:{minutes_start:02}')
                break

            send_time.append(f'{hours_start:02}:{minutes_start:02}')
            minutes_start += interval
    except Exception as e:
        logging.log(f'Ошибка в формировании списка интервалов отправки фото. Причина {e}', PrintToConsole, PrintToFile)

    logging.log(f'Список расписания отправки фото: {send_time}', PrintToFile)
    logging.log('Установка времени отправки => OK', PrintToFile)
else:
    logging.log('Ошибка! Нет обязательного пункта, добавьте в config.ini строку "TIME_SEND = 10:00 - 19:00"', PrintToFile)
    config_state = False

#  Установка периода ротации лог файла
if config_dict.get('LOG_FILE_ROTATE', False):
    log_file_period = int(config_dict['LOG_FILE_ROTATE'].strip('d'))
    logging.log(f'Период ротации лог файла: {log_file_period} день', PrintToFile)
else:
    logging.log(f'Период ротации лог файла не задан, используется значение по умолчанию: {log_file_period} день', PrintToFile)

#  Установка периода архивации сделанных фото
if config_dict.get('IMAGE_ARCHIVE_PERIOD', False):
    image_archive_period = config_dict['IMAGE_ARCHIVE_PERIOD'].strip('d')
    logging.log(f'Период архивации сделанных фото: {image_archive_period} день', PrintToFile)
else:
    logging.log(f'Значение периода архивации фото не установлено. Используется значение по умолчанию: {image_archive_period}', PrintToFile)


def path_check(path_dir: str):
    try:
        os.mkdir(f'{path_dir}{os_info.slash}test_mkdir')
        os.rmdir(f'{path_dir}{os_info.slash}test_mkdir')
        return True
    except FileNotFoundError:
        logging.log(f'Каталог не найден {path_dir} или не создан', PrintToConsole, PrintToFile)
        return False
    except PermissionError:
        logging.log(f'Нет доступа для создания папки или файла {path_dir}', PrintToConsole, PrintToFile)
        return False


#  Директория фото пользователя
if config_dict.get('IMAGE_USER_DIR', False):
    if path_check(config_dict['IMAGE_USER_DIR'].strip("'")):
        image_user_dir = config_dict['IMAGE_USER_DIR'].strip("'")
    else:
        config_state = False
else:
    config_state = False
    logging.log('Каталог для сохранения пользовательских фото не задан')


#  Директория фото по расписанию
if config_dict.get('IMAGE_SCHEDULE_DIR', False):
    if path_check(config_dict['IMAGE_SCHEDULE_DIR'].strip("'")):
        image_schedule_dir = config_dict['IMAGE_SCHEDULE_DIR'].strip("'")
    else:
        config_state = False
else:
    config_state = False
    logging.log('Каталог сохранения для фото по расписанию не задан')


#  Проверка на несовпадения путей директории пользовательских фото и фото по расписанию
if image_user_dir == image_schedule_dir:
    logging.log(f'Путь {image_user_dir} равен пути {image_schedule_dir}, установите разные папки', PrintToConsole, PrintToFile)
    config_state = False
else:
    logging.log(f'Установка каталога пользовательских фото => {image_user_dir}', PrintToConsole, PrintToFile)
    logging.log(f'Установка каталога фото по расписанию => {image_schedule_dir}', PrintToConsole, PrintToFile)


#  Директория фото архивации пользовательских фото
if config_dict.get('IMAGE_USER_ARCH_DIR', False):
    if path_check(config_dict['IMAGE_USER_ARCH_DIR'].strip("'")):
        image_user_arch_dir = config_dict['IMAGE_USER_ARCH_DIR'].strip("'")
        logging.log(f'Установка каталога архива пользовательких фото => {image_user_arch_dir}', PrintToConsole,
                    PrintToFile)
    else:
        config_state = False
else:
    config_state = False
    logging.log('Папка архива пользовательских фото не задана', PrintToConsole, PrintToFile)

#  Директория фото архивации фото по расписанию
if config_dict.get('IMAGE_SCHEDULE_ARCH_DIR', False):
    if path_check(config_dict['IMAGE_SCHEDULE_ARCH_DIR'].strip("'")):
        image_schedule_arch_dir = config_dict['IMAGE_SCHEDULE_ARCH_DIR'].strip("'")
        logging.log(f'Установка каталога архива фото по расписанию => {image_schedule_arch_dir}', PrintToConsole,
                    PrintToFile)
    else:
        config_state = False
else:
    config_state = False
    logging.log('Папка архива фото по расписанию не задана', PrintToConsole, PrintToFile)


#  Проверка конфига перед запуском
if config_state:
    logging.log('Проверка config.ini => Пройден проверку', PrintToFile, PrintToConsole)

else:
    logging.log('Проверка config.ini => ОШИБКА', PrintToFile, PrintToConsole)
    exit(-1)

