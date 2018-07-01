import hashlib
import json
import uuid

import requests


class CleverApi():
    def __init__(self, access_token, verison="5.73"):
        self.access_token = access_token
        self.api_verison = verison

        self.device_id = uuid.uuid4().hex[:16]
        self.user_id = None

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Клевер/2.1.1 (Redmi Note 3; "
            "Android 23; Scale/3.00; VK SDK 1.6.8; com.vk.quiz)".encode("utf-8")
        })

    def request(self, method, payload: dict):
        payload["access_token"] = self.access_token
        payload["v"] = self.api_verison
        content = self.session.post("https://api.vk.com/method/{}"
                                .format(method), data=payload).json()

        if "error" in content:
            raise Exception("api response has error: " + json.dumps(content))

        return content["response"]

    def get_long_poll(self, owner_id, video_id):
        payload = {"owner_id": owner_id, "video_id": video_id}
        return self.request("video.getLongPollServer", payload)

    def get_start_data(self):
        payload = {
            "build_ver": "40031",
            "need_leaderboard": "0",
            "func_v": "4",
            "lang": "ru",
            "https": "1"
        }
        return self.request("execute.getStartData", payload)

    def get_user(self):
        return self.request("users.get", dict())

    def __resolve_user_id(self):
        user = self.get_user()
        self.user_id = user[0]["id"]

    def get_hash(self, params: list):
        ids = ("".join(map(str, params)) + "3aUFMZGRCJ").encode("utf-8")
        ids_hash = hashlib.md5(ids).hexdigest()

        user = str(int(self.user_id) ^ 202520).encode("utf-8")
        user_hash = hashlib.md5(user).hexdigest()

        device = (str(self.device_id) + "0MgLscD6R3").encode("utf-8")
        device_hash = hashlib.md5(device).hexdigest()

        return "{}#{}#{}".format(ids_hash, user_hash, device_hash)

    def use_proxy(self, address):
        self.session.proxies = {
            "http": address,
            "https": address
        }

    def remove_proxy(self):
        self.session.proxies = dict()

    def send_action(self, action_id):
        if not self.user_id:
            self.__resolve_user_id()

        hash = self.get_hash([action_id])
        payload = {"action_id": action_id, "hash": hash}

        return self.request("streamQuiz.trackAction", payload)

    def send_action_watched_game(self):
        return self.send_action(1)

    def send_action_join_game(self):
        return self.send_action(2)

    def send_action_answer_correct(self):
        return self.send_action(3)

    def send_action_win_game(self):
        return self.send_action(4)

    def send_action_invite_friend(self):
        return self.send_action(5)

    def send_action_community_notify(self):
        return self.send_action(6)

    def send_action_aliexpress_auth(self):
        return self.send_action(8)

    def send_answer(self, coins_answer, game_id, answer_id, question_id):
        if game_id == 0:
            raise Exception("game_id must be non-zero")

        if not self.user_id:
            self.__resolve_user_id()

        hash = self.get_hash([game_id, question_id])
        payload = {
            "answer_id": answer_id,
            "question_id": question_id,
            "device_id": self.device_id,
            "hash": hash,
        }

        if coins_answer is True:
            payload["coins_answer"] = True

        return self.request("streamQuiz.sendAnswer", payload)
