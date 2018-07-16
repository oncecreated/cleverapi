import hashlib
import json
import uuid

import requests


class BaseCleverApi():
    def __init__(self, access_token, version="5.73"):
        self.access_token = access_token
        self.api_version = version

        self.device_id = uuid.uuid4().hex[:16]
        self.user_id = None

    def get_longpoll(self, owner_id, video_id):
        data = {"owner_id": owner_id, "video_id": video_id}
        return "video.getLongPollServer", data

    def get_start_data(self):

        data = {
            "build_ver": "40031",
            "need_leaderboard": "0",
            "func_v": "4",
            "lang": "ru",
            "https": "1"
        }

        return "execute.getStartData", data

    def get_user(self):
        return "users.get"

    def get_hash(self, params: list):
        ids = ("".join(map(str, params)) + "3aUFMZGRCJ").encode("utf-8")
        ids_hash = hashlib.md5(ids).hexdigest()

        user = str(int(self.user_id) ^ 202520).encode("utf-8")
        user_hash = hashlib.md5(user).hexdigest()

        device = (str(self.device_id) + "0MgLscD6R3").encode("utf-8")
        device_hash = hashlib.md5(device).hexdigest()

        return "{}#{}#{}".format(ids_hash, user_hash, device_hash)

    def send_action(self, action_id):
        hash = self.get_hash([action_id])
        data = {"action_id": action_id, "hash": hash}

        return "streamQuiz.trackAction", data

    def send_answer(self, coins_answer, game_id, answer_id, question_id):
        hash = self.get_hash([game_id, question_id])

        data = {
            "answer_id": answer_id,
            "question_id": question_id,
            "device_id": self.device_id,
            "hash": hash,
        }

        if coins_answer is True:
            data["coins_answer"] = True

        return "streamQuiz.sendAnswer", data

    def get_gifts(self):
        return "execute.getGifts"

    def purchase_gift(self, gift_id):
        data = {"gift_id": gift_id}
        return "streamQuiz.purchaseGift", data

    def use_extra_life(self):
        return "streamQuiz.useExtraLife"


class CleverApi(BaseCleverApi):
    def __init__(self, access_token, version="5.73"):
        super().__init__(access_token, version=version)

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Клевер/2.1.1 (Redmi Note 3; "
            "Android 23; Scale/3.00; VK SDK 1.6.8; com.vk.quiz)".encode("utf-8")
        })

    def fetch(self, method, data=dict()):
        data.update({
            "access_token": self.access_token,
            "v": self.api_version, 
            "lang": "ru",
            "https": 1
        })

        content = self.session.post("https://api.vk.com/method/{}"
                                    .format(method), data=data).json()

        if "error" in content:
            raise Exception("api response has error: " + json.dumps(content))

        return content["response"]

    def get_longpoll(self, owner_id, video_id):
        method, data = super().get_longpoll(owner_id, video_id)
        return self.fetch(method, data)

    def get_start_data(self):
        method, data = super().get_start_data()
        return self.fetch(method, data)

    def get_user(self):
        method = super().get_user()
        return self.fetch(method)

    def send_action(self, action_id):
        method, data = super().send_action(action_id)
        return self.fetch(method, data)

    def send_answer(self, coins_answer, game_id, answer_id, question_id):
        method, data = super().send_answer(coins_answer, game_id, answer_id, question_id)
        return self.fetch(method, data)

    def get_gifts(self):
        method = super().get_gifts()
        return self.fetch(method)

    def purchase_gitf(self, gift_id):
        method, data = super().purchase_gift(gift_id)
        return self.fetch(method, data)

    def use_extra_life(self):
        method = super().use_extra_life()
        return self.fetch(method)