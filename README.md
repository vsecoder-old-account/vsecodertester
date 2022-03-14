# vsecodertester API

Гибкое API для выполнения Python кода в контейнере Docker с ограничениями

## Install

```bash
pip install --upgrade pip && \ pip install -r requirements.txt
```

Сами скачайте Docker для своей системы

```bash
docker build -t "app:worker" .
```

Используйте файл api.py отдельно закоментировав тестовое выполнение кода в конце файла!

## Example

```python
print(
    API.start(
        'print(1)', # python code(str)
        memory=512,                         # память(в МБ) максимально доступная для выполнения(int)
        cpus=1,                             # кол-во ядер для выполнения(int)
        network_disabled=False,             # блокировка интернета (bool)
        t=5                                 # максимальное среднее время выполнения(int)
    )
)

# result =>

#{
#    'id': 534403284476367,            -- id
#    'code': 'print(1)',               -- python code
#    'result': '1\n',                  -- result
#    'status': 'None',                 -- status(if stopped - process killed)
#    'max': {                          -- limitations
#        'memory': '512MiB', 
#        'CPUS': '1', 
#        'time': '5s'
#    }, 
#    'usage': {
#        'memory': '0Mib',             -- usage peak (> 1 MB)
#        'CPUS': '0',                  -- usage peak (> 1)
#        'time': '0.6736643314361572s' -- execution time
#    }
#}
```
