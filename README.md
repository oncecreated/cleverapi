# **Clever API**
Библиотека созданная для удобного взаимодействия с API мобильного приложения Клевер, разрабатываемого во ВКонтакте.

## Установка
Протестирована работа с Python 3.6.

* Установка с помощью pip (пакетный менеджер Python):
```
$ pip install cleverapi
```
* Установка из исходного кода (требуется git)
```
$ git clone https://github.com/oncecreated/cleverapi.git
$ cd cleverapi
$ python setup.py install
```

## Использование
Пользоваться библиотекой очень просто. Например, для вывода текста вопроса из онлайн-викторины потребуется всего несколько строчек кода:

```python
import cleverapi

api = CleverApi("TOKEN")
lp = CleverLongPoll(api)

@lp.question_handler()
def new_question(event):
    print(event["question"]["text"])

lp.game_waiting()
```
