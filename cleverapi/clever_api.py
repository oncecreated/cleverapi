import hashlib
import json
import uuid

import requests
import aiohttp

from .exceptions import ApiResponseError
from .action import Action


class BaseCleverApi():
    def __init__(self, access_token, version="5.73"):
        self.access_token = access_token
        self.api_version = version
        self.device_id = uuid.uuid4().hex[:16]
        self.api_host = "api.vk.com"

    def fetch(self, method, data=None):
        if data is None:
            data = {}

        return method, data

    def get_longpoll(self, owner_id, video_id):
        data = {"owner_id": owner_id, "video_id": video_id}
        return self.fetch("video.getLongPollServer", data)

    def get_start_data(self):
        data = {
            "build_ver": "503028",
            "need_leaderboard": "0",
            "func_v": "6",
            "lang": "ru",
            "https": "1"
        }
        return self.fetch("execute.getStartData", data)

    def get_user(self):
        return self.fetch("users.get")

    def get_hash(self, additional: list, user_id):
        ids = "".join(map(str, additional)) + "3aUFMZGRCJ"
        ids_hash = hashlib.md5(ids.encode()).hexdigest()

        user = str(int(user_id) ^ 202520)
        user_hash = hashlib.md5(user.encode()).hexdigest()

        device = str(self.device_id) + "0MgLscD6R3"
        device_hash = hashlib.md5(device.encode()).hexdigest()

        return "{}#{}#{}".format(ids_hash, user_hash, device_hash)
    
    def bump(self, lat, lon):
        data = {"lat": lat, "lon": lon, "prod": 1, "func_v": 1}
        return self.fetch("execute.bump", data)
    
    def send_action(self, *, action_id: Action, user_id):
        secure_hash = self.get_hash([action_id.value], user_id)
        data = {"action_id": action_id.value, "hash": secure_hash}

        return self.fetch("streamQuiz.trackAction", data)

    def send_answer(self, *, coins_answer: bool, game_id, answer_id, question_id, user_id):
        secure_hash = self.get_hash([game_id, question_id], user_id)

        data = {
            "answer_id": answer_id,
            "question_id": question_id,
            "device_id": self.device_id,
            "hash": secure_hash,
        }

        if coins_answer:
            data["coins_answer"] = True

        return self.fetch("streamQuiz.sendAnswer", data)

    def get_gifts(self):
        return self.fetch("execute.getGifts")

    def purchase_gift(self, gift_id):
        data = {"gift_id": gift_id}
        return self.fetch("streamQuiz.purchaseGift", data)

    def get_daily_rewards(self):
        return self.fetch("streamQuiz.getDailyRewardsData")
    
    def get_train_questions(self):
        return self.fetch("streamQuiz.getTrainQuestions")
    
    def use_extra_life(self):
        return self.fetch("streamQuiz.useExtraLife")

    def get_nearby_users(self, lat, lon):
        data = {"lat": lat, "lon": lon}
        return self.fetch("execute.getNearbyUsers", data)

    def comment(self, *, owner_id, video_id, message):
        data = {
            "owner_id": owner_id,
            "video_id": video_id,
            "message": message
        }

        return self.fetch("execute.createComment", data)


class CleverApi(BaseCleverApi):
    def __init__(self, access_token, version="5.73"):
        super().__init__(access_token, version=version)

        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Клевер/2.3.3 (Redmi Note 5; "
            "Android 28; VK SDK 1.6.8; com.vk.quiz)".encode(
                "utf-8")
        })

    def fetch(self, method, data=None):
        if data is None:
            data = {}

        data.update({
            "access_token": self.access_token,
            "v": self.api_version,
            "lang": "ru",
            "https": 1
        })

        url = f"https://{self.api_host}/method/{method}"

        content = self.session.post(url, data=data).json()
        error = content.get("error")

        if error is not None:
            raise ApiResponseError(json.dumps(content))

        return content["response"]


class AsyncCleverApi(BaseCleverApi):
    def __init__(self, access_token, connector, version="5.73"):
        super().__init__(access_token, version=version)

        self.connector = connector

    async def fetch(self, method, data=None):
        if data is None:
            data = {}
        
        data.update({
            "access_token": self.access_token,
            "v": self.api_version,
            "lang": "ru",
            "https": 1
        })

        url = f"https://{self.api_host}/method/{method}"

        async with self.connector.session.post(url, data=data) as response:

            content = await response.json()
            error = content.get("error")

            if error is not None:
                raise ApiResponseError(json.dumps(content))

            return content["response"]
