import sys
import json

sys.path.append('../')

import pytest
from cleverapi import CleverApi


@pytest.fixture
def api():
    return CleverApi(None)


def test_hash_action(api):
    api.user_id = "91670994"
    api.device_id = "77a3af1dbf002b1b"
    hash = api.get_hash(["6"])

    assert hash == "8cc151519e41f560bf93b02278413875#"
    "5c75528a585768893d29c137b342057f#"
    "34f1d74e8991b6687a296f6a8c8c92a7"


def test_hash_answer(api):
    api.user_id = "91670994"
    api.device_id = "77a3af1dbf002b1b"
    hash = api.get_hash(["215", "18"])

    assert hash == "f892054ed677ea5a654aa25606ea045d#"
    "5c75528a585768893d29c137b342057f#"
    "34f1d74e8991b6687a296f6a8c8c92a7"


def test_send_answer_with_zero_game_id(api):
    with pytest.raises(Exception) as exception:
        api.send_answer(True, 0, 1, 1)

    assert "game_id must be non-zero" in str(exception.value)
