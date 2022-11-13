# foto_to_telegram
<p align="center">Телеграм бот предназначенный для отправки фото с веб или usb камер в чат или в личные сообщения с заданным интервалом времени</p>
<p>
<p>
<p align="center"><b>Установка на Linux:</b></p>
<p align="center"><b>На примере Ubuntu 20</b></p>

1. Установить Python, в консоли пишем <b>sudo apt-get install python3</b>
2. Установить pip3, <b>sudo apt-get install python3-pip</b>
3. Установить git, <b>sudo apt-get install git</b>
4. Клонируем репозиторий проекта - <b>sudo git clone https://github.com/rudikrudik/foto_to_telegram.git</b>
5. Устанавливаем зависимости, <b>pip3 install -r requirements.txt</b>
    + В ubuntu необходимо установить 24 часовой формат времени - <b>localectl set-locale LC_TIME=en_EN.UTF-8</b>
    + Временная зона - <b>sudo timedatectl set-timezone Europe/Moscow</b>
7. Переименовываем файл <b>config_ini.example</b> в <b>config.ini</b>
8. В <b>config.ini</b> прописываем пути где будут храниться сделанные фото и архивы
    + В директории <b>IMAGE_USER_DIR</b> путь фото сделанных по запросу от пользователя. Пример <b>/user/home/camera/user_foto</b>
    + В директории <b>IMAGE_SCHEDULE_DIR</b> путь фото сделанных по расписанию.
       - Эти две директории должны отличаться 
    + В директории <b>IMAGE_USER_ARCH_DIR</b> и <b>IMAGE_SCHEDULE_ARCH_DIR</b> пути где будут храниться архивы фото
9. Так же в конфигурационном файле правим параметры по необходимости.
    + Обязательно вписываем свой токен телеграм бота полученный от Bot Father
    + Функционал уровней логирования <b>LOG_LEVEL</b> еще не реализован
10. Запускаем программу - <b>python3 main.py</b>
11. В случае каких либо ошибок просмотреть лог файл.

<p align="center"><b>Запуск как сервиса:</b></p>
1. Создаем файл <b>touch /etc/systemd/system/foto_to_telegram_bot.service</b> следуюещго содержания:


      [Unit]
      Description=Foto to Telegram Python Bot

      [Service]
      Type=simple
      ExecStart=/usr/bin/python3 /path/to/programm/main.py
      WorkingDirectory=/path/to/programm
      Restart=always
      RestartSec=30

      [Install]
      WantedBy=multi-user.target


2. Пишем команды:

       sudo systemctl enable foto_to_telegram_bot.service
       sudo systemctl daemon-reload
       sudo systemctl start foto_to_telegram_bot.service
      
3. По не понятным мне причинам PyTelebotApi очень странно себя ведет если его не перезапускать. Поэтом я в cron добавил перезапуск сервиса раз в час

       0 */1 * * * systemctl restart foto_to_telegram_bot.service
       

<p align="center"><b>Применение</b></p>
На данный момент бот применяется в одном из магазинов для контроля очередей. Позволяет не "бегать" по магазину и не тратить время на отчетность и заполнение бумаг.</br>
Может применяться для создания таймлапсов, за наблюдением изменения обьекта в случае больших временных интервалов.<br>
<p>
Если не получатся запустить или возникли вопросы пишите в телеграм - https://t.me/rudik_rudik

      
