import json
import random
import time

import requests

from cleverapi import CleverApi, CleverLongPoll

access_token = "TOKEN"
api = CleverApi(access_token)
lp = CleverLongPoll(api)

friends_answers = [0, 0, 0]


# обработчик вопросов
@lp.question_handler()
def new_question(event):
    global friends_answers
    friends_answers = [0, 0, 0]


# обработчик ответов друзей
@lp.friend_answer_handler()
def count_friend_answers(event):
    print(event)
    answer_id = event["answer_id"]
    friends_answers[answer_id] += 1


# обработчик вызывающийся по истечении времени отведенного на ответ
@lp.last_time_answer_handler()
def give_answer(event):
    majority_answer = max(friends_answers)

    if friends_answers.count(majority_answer) == 1:
        majority_answer = friends_answers.index(majority_answer)
    else:
        majority_answer = random.randint(0, 2)

    question_id = event["question"]["id"]
    print(api.send_answer(lp.game_id, majority_answer, question_id))


# обработчик события правильного ответа
@lp.right_answer_handler()
def give_actions(event):
    print(api.send_action_answer_correct())


lp.game_waiting()
