import shutil
import os
import threading


from os_info import OsInfo


class FotoMove(OsInfo):

    def __init__(self, schedule_foto_dir: str, user_foto_dir: str):
        super().__init__()
        self.schedule_foto_dir = schedule_foto_dir
        self.user_foto_dir = user_foto_dir

    def user_foto(self, camera: int):
        self.__move(camera, self.user_foto_dir)

    def schedule_foto(self, camera: int):
        self.__move(camera, self.schedule_foto_dir)

    def __move(self, cam: int, directory: str):
        shutil.copy(f'cam{cam}.jpg', f'{directory}{self.slash}{self.get_time_stamp()}_cam{cam}.jpg')


class FotoZip(OsInfo):

    def __init__(self, src_dir: str, dst_dir: str):
        super().__init__()
        self.src_dir = src_dir
        self.dst_dir = dst_dir

    def foto_zip(self):
        os.rename(f'{self.src_dir}', f'{self.src_dir}' + '_arh')
        os.mkdir(f'{self.src_dir}')
        shutil.make_archive(f'{self.dst_dir}{self.slash}{self.get_time_stamp()}_arh', 'zip', f'{self.src_dir}' + '_arh')

        shutil.rmtree(f'{self.src_dir}' + '_arh')

    def run(self):
        thread = threading.Thread(target=self.foto_zip, args=())
        thread.daemon = False
        thread.start()
