# **Clever API**
Библиотека созданная для удобного взаимодействия с API мобильного приложения Клевер, разрабатываемого во ВКонтакте.

## Навигация
- [Установка](#Установка)
- [Использование](#Использование)
- [Получение токена](#Получение-токена)
- [Обработчики](#Обработчики)
- [Действия](#Действия)
- [Отправка ответа](#Отправка-ответа)
- [Бамп](#Бамп)
- [События](#События)
    - [sq_game_winners](#sq_game_winners)
    - [sq_friend_answer](#sq_friend_answer)
    - [sq_question](#sq_question)
    - [sq_ed_game](#sq_ed_game)
    - [sq_question_answers_right](#sq_question_answers_right)
    - [video_comment_new](#video_comment_new)
- [Примеры](#Примеры)

## Установка
Протестирована работа с Python 3.6.

* Установка с помощью pip (пакетный менеджер Python):
```
$ pip install cleverapi --upgrade
```
* Установка из исходного кода (требуется git)
```
$ git clone https://github.com/oncecreated/cleverapi.git
$ cd cleverapi
$ python setup.py install
```

## Использование
Вывод текста вопроса из онлайн викторины:

```python
from cleverapi import CleverApi, CleverLongPoll

api = CleverApi("TOKEN")
lp = CleverLongPoll(api)

@lp.question_handler()
def new_question(event):
    print(event["question"]["text"])

lp.game_waiting()
```
Главной точкой взаимодействия библиотеки с Клевером, является **CleverLongPoll** реализуемый библиотекой. С помощью него становится возможным в реальном времени получать игровые события, будь то ответ вашего друга или новый вопрос.

## Получение токена
Для работы библиотеки необходимо получить access_token приложения Клевер, сделать это можно воспользовавшись ссылкой (access_token будет в адресной строке после подтверждения прав доступа):

`http://oauth.vk.com/authorize?client_id=6334949&scope=589842&display=mobile&response_type=token`

## Обработчики
Поступающие игровые события нужно как-то обрабатывать, для этого нужно использовать специальные обработчики.

Обработчиком становится функция перед которой установлен определенный декоратор. К примеру, если вы захотите получать список победителей игры в вашей функции, то можно воспользоваться следующей конструкцией:

```python
@lp.game_winners_handler()
def print_winners(event):
    print(event)
```

У функции после декоратора должен быть единственный параметр, отвечающий за информацию о событии.

Список доступных декораторов:

|Декоратор | Тип события | Описание|
|---|---|---|
| `comment_handler`| `video_comment_new`|Событие комментария к игровой трансляции|
| `question_handler`|`sq_question`|Событие нового вопроса|
| `friend_answer_handler`|`sq_friend_answer`|Событие ответа друга пользователя|
| `right_answer_handler`|`sq_question_answers_right`|Событие результата ответа на вопрос|
| `end_game_handler`|`sq_ed_game`|Событие окончания викторины|
| `game_winners_handler`| `sq_game_winners` |Событие списка победивших игроков |
| `start_game_handler`|-|Дополнительный декоратор, сигнализирует о начале игры |
| `all_events_handler`|-|Дополнительный декоратор, служит для получения всех событий пришедших с LongPoll |
| `last_time_answer`|`sq_question`|Дополнительный декоратор, вызываемый в последнее возможное время ответа на вопрос (может быть полезно, когда нужно ответить не сразу после получения вопроса) |


## Действия
В игре существуют некоторые действия, за которые вам начисляют клеверсы. Для начисления виртуальных монеты необходимо самостоятельно вызывать метод **send_action***.

В параметрах необходимо передать тип действия (**cleverapi.Action**) и идентификатор пользователя.

Например, если вы правильно ответили на вопрос, то не забудьте оповестить об этом сервер:
```python
from cleverapi import Action
api.send_action(Action.ANSWER_CORRECT)
```

Список возможных действий:

|Действие | Описание|
|---|---|
| `Action.WATCHED_GAME`|Вы досмотрели игру до конца|
| `Action.JOIN_GAME`|Вы присоединились к игре|
| `Action.ANSWER_CORRECT`|Вы дали правильный ответ|
| `ACtion.WIN_GAME`|Вы выиграли игру|
| `Action.INVITE_FRIEND`|Вы пригласили друга|
| `Action.COMMUNITY_NOTIFY`|Вы подписались на уведомления сообщества Клевер|

## Отправка ответа
Для отправки ответа используется метод. **send_answer**:
```python
api.send_answer(coins_answer, game_id, answer_id, question_id)
```
Параметры метода:
- `coins_answer` (`bool`) - Передавайте True если играете на клеверсы, передавайте значение False, если вы продолжаете играть на деньги. *Осторожно, если вы передадите значение False когда уже выбыли из игры ваш ответ не будет засчитан*
- `game_id` (`int`) - идентификатор текущей игры, его можно получить из атрибута `game_id` класса `CleverLongPoll`

## Бамп
Для бампа используется метод. **bump**:
```python
api.bump(lat, lon)
```
Параметры метода:
- `lat` (`string`) - Широта
- `lon` (`string`) - Долгота

Передаются в виде градусов (xx.xxxxxx)

Внимание: За 1 бамп с 1 человеком дают 50 клеверсов, с 1 человеком можно бампится 1 раз в неделю. Лимит бампов в неделю: 1000 клеверсов.

## Покупка в магазине за клеверсы
Для получения списка товаров с магазина используется метод. **getGifts**.
```python
gifts = api.get_gifts()
print(gifts)
```
Покупка товара: **purchaseGift**
```python
api.purchase_gift(1)
```1
Где цифра 1 это ID товара. В нашем случае это жизнь.
## События
Игровые события в формате JSON.

### **sq_game_winners** 
```json
{  
   "type":"sq_game_winners",
   "owner_id":-162894513,
   "video_id":456230000,
   "users":[  
      {  
         "name":"Самира В.",
         "photo_url":"https://vk.com/images/camera_200.png?ava=1"
      },
      {  
         "name":"Владислав П.",
         "photo_url":"https://vk.com/images/camera_200.png?ava=1"
      },
      {  
         "name":"Варвара Д.",
         "photo_url":"https://vk.com/images/camera_200.png?ava=1"
      },
      {  
         "name":"Анастасия Ф.",
         "photo_url":"https://vk.com/images/camera_200.png?ava=1"
      },
      {  
         "name":"Тёма Б.",
         "photo_url":"https://vk.com/images/camera_200.png?ava=1"
      },
      {  
         "name":"Евгений В.",
         "photo_url":"https://vk.com/images/camera_200.png?ava=1"
      },
      {  
         "name":"Вячеслав З.",
         "photo_url":"https://vk.com/images/camera_200.png?ava=1"
      },
      {  
         "name":"Дарья М.",
         "photo_url":"https://vk.com/images/camera_200.png?ava=1"
      },
      {  
         "name":"Светлана С.",
         "photo_url":"https://vk.com/images/camera_200.png?ava=1"
      }
   ],
   "prize":0,
   "winners_num":9,
   "version":2
}
```

### **sq_friend_answer** 
Необходимо купить их отображение за 299 клеверсов (id подарка 50)
```json
{  
   "type":"sq_friend_answer",
   "game_id":200,
   "user_id":100,
   "answer_id":0,
   "photo_url":"https://vk.com/images/camera_200.png?ava=1",
   "is_live_enabled":true
}
```

### **sq_question** 
```json
{  
   "type":"sq_question",
   "owner_id":-162894513,
   "video_id":456239000,
   "question":{  
      "id":11,
      "text":"Кто основал социальную сеть ВКонтакте?",
      "answers":[  
         {  
            "id":0,
            "text":"Николай Дуров"
         },
         {  
            "id":1,
            "text":"Павел Дуров"
         },
         {  
            "id":2,
            "text":"Илон Маск"
         }
      ],
      "time":null,
      "number":1
   },
   "version":2
}
```

### **sq_ed_game**
```json
{  
   "type":"sq_ed_game",
   "owner_id":-162894513,
   "video_id":456230000,
   "version":2
}
```

### **sq_question_answers_right**
```json
{  
   "type":"sq_question_answers_right",
   "owner_id":-162894513,
   "video_id":456230000,
   "question":{  
      "text":"Кто основал социальную сеть ВКонтакте?",
      "answers":[  
         {  
            "id":0,
            "text":"Николай Дуров",
            "users_answered":1584
         },
         {  
            "id":1,
            "text":"Павел Дуров",
            "users_answered":389217
         },
         {  
            "id":2,
            "text":"Илон Маск",
            "users_answered":389
         }
      ],
      "right_answer_id":1,
      "id":11,
      "is_first":true,
      "is_last":false,
      "number":1,
      "sent_time":1529600002,
      "answer_set":true
   },
   "question_time":1529600000,
   "version":2
}
```

### **video_comment_new**
```json
{  
   "type":"video_comment_new",
   "owner_id":-162894513,
   "video_id":456230000,
   "comment":{  
      "id":0,
      "from_id":100,
      "date":152960000,
      "text":"мыши"
   },
   "user":{  
      "id":100,
      "photo_50":"https://vk.com/images/camera_200.png?ava=1",
      "photo_100":"https://vk.com/images/camera_200.png?ava=1",
      "first_name":"Павел",
      "last_name":"Анисимов",
      "sex":2
   },
   "version":2
}
```

## Примеры
[like_friends.py](https://github.com/oncecreated/cleverapi/blob/master/examples/like_friends.py) - использование библиотеки для создания бота, который выбирает наиболее популярный ответ у друзей
[bump.py](https://github.com/oncecreated/cleverapi/blob/master/examples/bump.py) - использование библиотеки для бампа, который происходит в выбранных координатах
