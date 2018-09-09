import json
import random
import time

import requests

from cleverapi import CleverApi, CleverLongPoll, Action

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
    answer_id = event["answer_id"]
    friends_answers[answer_id] += 1

last_answer = None

# обработчик вызывающийся по истечении времени отведенного на ответ
@lp.last_time_answer_handler()
def give_answer(event):
    majority_answer = max(friends_answers)

    if friends_answers.count(majority_answer) == 1:
        answer = friends_answers.index(majority_answer)
    else:
        answer = random.randint(0, 2)

    question_id = event["question"]["id"]
    response = api.send_answer(True, lp.game_id, answer, question_id, lp.user_id)

    if response == 1:
        global last_answer
        last_answer = answer


# обработчик события правильного ответа
@lp.right_answer_handler()
def give_actions(event):
    question = event["question"]
    
    # если ответ совпал с правильным вызываем действие награды
    if question["right_answer_id"] == last_answer:
        api.send_action(Action.ANSWER_CORRECT, lp.user_id)


lp.game_waiting()
