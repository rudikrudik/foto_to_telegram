import time
import platform


class OsInfo:

    def __init__(self):
        if platform.system() == 'Windows':
            self.slash = '\\'
        elif len(platform.system()) == 0:
            self.slash = '/'
        else:
            self.slash = '/'
        self.prefix = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    @staticmethod
    def get_time_stamp() -> str:
        return time.strftime('%Y-%m-%d_%H_%M', time.localtime())

    @staticmethod
    def get_time() -> str:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    @staticmethod
    def time_format() -> str:
        return time.strftime('%H:%M', time.localtime())
