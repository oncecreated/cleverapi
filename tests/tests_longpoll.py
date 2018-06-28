import sys
import json

sys.path.append('../')

import pytest
from cleverapi import CleverLongPoll

@pytest.fixture
def longpoll():
    return CleverLongPoll(None)


def test_event_parsing(longpoll):
    with open("./testdata/raw_events.json", "r") as file:
        file_content = file.read()
        raw_events_array = json.loads(file_content)
        events = longpoll.decode_event(raw_events_array)

    assert len(events) == 2


def test_start_game_state(longpoll):
    assert longpoll.is_in_game == False


def test_game_state_clear(longpoll):
    longpoll.is_in_game = True
    longpoll.game_id = 123

    longpoll.clear_game_state()

    assert longpoll.is_in_game == False
    assert longpoll.game_id == 0


def test_end_polling(longpoll):
    longpoll.is_in_game = True

    with open("./testdata/end_game_event.json", "r") as file:
        file_content = file.read()
        end_game_event = json.loads(file_content)
        longpoll.process_event(end_game_event)

    assert longpoll.is_in_game == False


def test_url_update(longpoll):

    with open("./testdata/longpoll_url.txt", "r") as file:
        file_content = file.read()
        longpoll.update_url(file_content)

    assert longpoll.endpoint == "https://queuev4.vk.com/im319"
    assert longpoll.parameters["act"] == "a_check"
    assert longpoll.parameters["key"] == "EaU0rQEMbXHGiKvXgC60JLOSb6L1"
    assert longpoll.parameters["ts"] == "1162020000"
    assert longpoll.parameters["wait"] == "25"
    assert longpoll.parameters["id"] == "100"


def test_handler_notify(longpoll):
    #pylint: disable=unused-variable

    @longpoll.end_game_handler()
    def default_handler(event):
        event["type"] = "notified"

    with open("./testdata/end_game_event.json", "r") as file:
        file_content = file.read()
        end_game_event = json.loads(file_content)
        longpoll.process_event(end_game_event)

    assert end_game_event["type"] == "notified"


def test_all_handler_notify(longpoll):
    #pylint: disable=unused-variable

    @longpoll.all_events_handler()
    def default_handler(event):
        event["type"] = "notified"

    with open("./testdata/end_game_event.json", "r") as file:
        file_content = file.read()
        impossible_event = json.loads(file_content)
        impossible_event["type"] = "impossible_type"
        longpoll.process_event(impossible_event)

    assert impossible_event["type"] == "notified"