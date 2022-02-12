# vsecodertester

## Install

Need install python and docker!

```bash
git clone https://github.com/vsecoder/vsecodertester
docker build -t "app:worker" .
```

И уже в зависимости от задач запускайте bot.py или main.py:

```bash
python .py
```

## TODO

1. Переделать на docker библиотеку с subprocess
2. Добавить поддержку разных языков
3. Установить на мощный сервер и протестить под большими нагрузками
