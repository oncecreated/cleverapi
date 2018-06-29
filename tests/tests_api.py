import sys
import json

sys.path.append('../')

import pytest
from cleverapi import CleverApi
from testdata import hashes

@pytest.fixture
def api():
    return CleverApi(None)

def test_hash_action(api):
    api.user_id = "91670994"
    api.device_id = "77a3af1dbf002b1b"
    hash = api.get_hash(["6"])

    assert hash == hashes.action_test_hash

def test_hash_answer(api):
    api.user_id = "91670994"
    api.device_id = "77a3af1dbf002b1b"
    hash = api.get_hash(["215", "18"])

    assert hash == hashes.answer_test_hash

def test_send_answer_with_zero_game_id(api):
    with pytest.raises(Exception) as exception:
        api.send_answer(True, 0, 1, 1)

    assert "game_id must be non-zero" in str(exception.value)
