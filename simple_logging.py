import sys
import threading
import zipfile

from os_info import OsInfo
from zipfile import ZipFile


class Logging:

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, 'instance'):
            cls.instance = super(Logging, cls).__new__(cls)
        return cls.instance

    def __init__(self, logfile_dst):
        self.logfile_dst = logfile_dst

    def log(self, message: str, *args):
        for arg in args:
            arg(self.logfile_dst).write(f"{message}")


class PrintToConsole:

    def __init__(self, logfile_dst_dir: str):
        self.logfile_dst_dir = logfile_dst_dir

    @staticmethod
    def write(message: str):
        sys.stderr.write(f'{message}\n')


class PrintToFile(OsInfo):

    def __init__(self, logfile_dst_dir: str):
        super().__init__()
        self.logfile_dst_dir = logfile_dst_dir
        self.lock = threading.Lock()

    def write(self, message: str):
        with self.lock:
            with open(f'{self.logfile_dst_dir}{self.slash}log.txt', 'a+', encoding='UTF8') as logfile:
                logfile.write(f'{self.get_time()} {message}\n')


class LogRotate(OsInfo):

    def __init__(self, logfile_dir):
        super().__init__()
        self.lock = threading.Lock()
        self.logfile_dir = logfile_dir

    def zip(self) -> None:
        with ZipFile(f'{self.logfile_dir}{self.slash}{self.get_time_stamp()}.zip', 'w', zipfile.ZIP_BZIP2) as zip_obj:
            zip_obj.write(f'{self.logfile_dir}{self.slash}log.txt', arcname='log.txt')
            with self.lock:
                with open(f'{self.logfile_dir}{self.slash}log.txt', 'w') as new_log:
                    new_log.write(f'{self.get_time()} ---- Новый лог файл создан ----\n')
