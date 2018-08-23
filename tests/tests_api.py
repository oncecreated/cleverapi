import sys
import json

sys.path.append('../')

import pytest
from cleverapi import BaseCleverApi, CleverApi


@pytest.fixture
def base_api():
    return BaseCleverApi(None)


def test_get_longpoll(base_api):
    method, data = base_api.get_longpoll("100", "1672345")

    assert method == "video.getLongPollServer"
    assert data == dict(owner_id="100", video_id="1672345")


def test_get_start_data(base_api):
    method, data = base_api.get_start_data()

    assert method == "execute.getStartData"
    assert data == dict(build_ver="40031", need_leaderboard="0", 
                    func_v="4", lang="ru", https="1")


def test_get_user(base_api):
    method, _ = base_api.get_user()

    assert method == "users.get"


def test_get_gifts(base_api):
    method, _ = base_api.get_gifts()

    assert method == "execute.getGifts"


def test_purchase_gift(base_api):
    method, data = base_api.purchase_gift(1)

    assert method == "streamQuiz.purchaseGift"
    assert data == dict(gift_id=1)


def test_use_extra_life(base_api):
    method, _ = base_api.use_extra_life()

    assert method == "streamQuiz.useExtraLife"

@pytest.fixture
def base_api_with_ids():
    api = BaseCleverApi(None)
    api.user_id = "91670994"
    api.device_id = "77a3af1dbf002b1b"
    return api


def test_hash_action(base_api_with_ids):
    
    hash = base_api_with_ids.get_hash(["6"])

    assert hash == str('8cc151519e41f560bf93b02278413875#'
                       '5c75528a585768893d29c137b342057f#'
                       '34f1d74e8991b6687a296f6a8c8c92a7')


def test_hash_answer(base_api_with_ids):
    hash = base_api_with_ids.get_hash(["215", "18"])

    assert hash == str('f892054ed677ea5a654aa25606ea045d#'
                       '5c75528a585768893d29c137b342057f#'
                       '34f1d74e8991b6687a296f6a8c8c92a7')


def test_send_action(base_api_with_ids):
    method, data = base_api_with_ids.send_action(6)

    assert method == "streamQuiz.trackAction"
    assert data == dict(action_id=6, hash=str('8cc151519e41f560bf93b02278413875#'
                '5c75528a585768893d29c137b342057f#34f1d74e8991b6687a296f6a8c8c92a7'))


def test_send_answer_for_money(base_api_with_ids):
    method, data = base_api_with_ids.send_answer(False, 215, 0, 18)

    assert method == "streamQuiz.sendAnswer"
    assert data == dict(answer_id=0, question_id=18, device_id="77a3af1dbf002b1b", 
        hash=str('f892054ed677ea5a654aa25606ea045d#5c75528a585768893d29c137b342057f#'
        '34f1d74e8991b6687a296f6a8c8c92a7'))


def test_send_answer_for_coins(base_api_with_ids):
    method, data = base_api_with_ids.send_answer(True, 215, 0, 18)

    assert method == "streamQuiz.sendAnswer"
    assert data == dict(answer_id=0, question_id=18, device_id="77a3af1dbf002b1b", 
        hash=str('f892054ed677ea5a654aa25606ea045d#5c75528a585768893d29c137b342057f#'
        '34f1d74e8991b6687a296f6a8c8c92a7'), coins_answer=True)


@pytest.fixture
def base_api_withput_ids():
    api = BaseCleverApi(None)
    return api


def test_get_hash_without_user_id(base_api_withput_ids):
    with pytest.raises(AttributeError):
        base_api_withput_ids.get_hash(["0"])




