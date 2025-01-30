# jazz_bot
Бот, который ежедневно ищет джазовые концерты за сегодняшний день в москве 
и публикует в телеграм канал
## пример сообщения
![](image.png)
# Как запустить
После скачивания репозитория перейдите в папку src
```commandline
cd src
```
создайте файл .env  с переменными окружения
```requirements
BOT_TOKEN=example:example
CHANEL_NAME=@example
```
скачайте необходимые зависимости
```commandline
pip install -r requirements.txt
```
запустите скрипт
```commandline
python main.py
```