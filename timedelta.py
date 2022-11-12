import os

import readconfig as rc
from os_info import OsInfo
from datetime import datetime
from simple_logging import Logging, PrintToConsole

logging = Logging(rc.log_file_dir)


class CheckRotate(OsInfo):

    def __init__(self):
        super().__init__()

    def check_foto(self, check_dst_dir: str, interval: int):
        try:
            list_dir = os.listdir(f'{check_dst_dir}')
            if len(list_dir) == 0:
                logging.log(f'Каталог: {check_dst_dir} пуст', PrintToConsole)
                return False
        except FileNotFoundError:
            logging.log(f'Каталог: {check_dst_dir} не найден', PrintToConsole)
            return False

        for img in list_dir:
            img_split = img[:10].split('-')
            time_diff = datetime.now() - (datetime(int(img_split[0]), int(img_split[1]), int(img_split[2])))
            if time_diff.days >= int(interval):
                return True
            else:
                return False

    def check_logfile(self, log_file_dir: str, interval: int):
        try:
            with open(f'{log_file_dir}{self.slash}log.txt', 'r', encoding='UTF-8') as dst_file:
                time_in_log = []
                for line in dst_file:
                    time_in_log = line[:10].split('-')
                    break

            time_diff = datetime.now() - (datetime(int(time_in_log[0]), int(time_in_log[1]), int(time_in_log[2])))
            if time_diff.days >= int(interval):
                return True
            else:
                return False
        except FileNotFoundError:
            logging.log('Файл log.txt не найден', PrintToConsole)
            return False
