import json
import time
import urllib.parse
from collections import OrderedDict
from threading import Timer

import requests

from .clever_api import CleverApi
from .exceptions import LongPollException


class CleverLongPoll():
    def __init__(self, api: CleverApi):
        self.api = api
        self.handlers = {}
        self.is_in_game = False
        self.game_id = 0

    def get_events(self):
        data = urllib.parse.urlencode(self.parameters)
        url = "{}?{}".format(self.endpoint, data)
        content = self.api.session.post(url).text
        response = json.loads(content)

        if "failed" in response:
            raise LongPollException("long poll response: " + content)

        # ts is longpoll request id
        # its change after each request
        self.parameters["ts"] = response["ts"]

        events = self.decode_event(response["events"])
        return events

    def decode_event(self, raw_events):
        events = []
        for event in raw_events:
            events.append(json.loads(event.split("<!>")[0]))
        return events

    def update_url(self, url):
        parsed = urllib.parse.urlparse(url)
        parameters = urllib.parse.parse_qs(parsed.query)

        self.parameters = OrderedDict()
        for key, value in parameters.items():
            self.parameters[key] = value[0]

        self.endpoint = "{}://{}{}".format(parsed.scheme,
                                           parsed.netloc, parsed.path)

    def game_waiting(self):
        retry_interval = .5

        while True:
            try:
                response = self.api.get_start_data()
                game = response["game_info"]["game"]
                game_status = game["status"]

                if game_status == "started":
                    self.__start_polling(game)

                elif game_status == "planned":
                    current_time = int(response["server_time"])
                    next_game_time = int(game["start_time"])
                    time.sleep(next_game_time - current_time)

                retry_interval = .5

            except requests.ConnectionError:
                time.sleep(retry_interval)
                retry_interval *= 2

    def __start_polling(self, game):
        self.is_in_game = True
        self.game_id = game["game_id"]
        url = self.api.get_longpoll(
            game["video_owner_id"], game["video_id"])["url"]

        self.update_url(url)

        if "__start_game" in self.handlers:
            self.notify_hadlers(game, self.handlers["__start_game"]) 

        self.event_loop()

    def event_loop(self):
        retry_interval = .5

        while self.is_in_game:
            try:
                events = self.get_events()
                for event in events:
                    self.process_event(event)

                retry_interval = .5

            except requests.ConnectionError:
                time.sleep(retry_interval)
                retry_interval *= 2

            except LongPollException:
                self.clear_game_state()
                return

    def process_event(self, event):
        event_type = event["type"]

        if event_type in self.handlers:
            self.notify_hadlers(event, self.handlers[event_type])
        
        if "__all__" in self.handlers:
            self.notify_hadlers(event, self.handlers["__all__"])

        if event_type == "sq_question":
            if "last_time_answer" in self.handlers:
                notify_later = Timer(10, self.notify_hadlers,
                                     (event, self.handlers["last_time_answer"]))
                notify_later.start()

        if event_type == "sq_ed_game":
            self.clear_game_state()

    def clear_game_state(self):
        self.game_id = 0
        self.is_in_game = False

    def notify_hadlers(self, event, handlers):
        for handler in handlers:
            handler(event)

    def custom_handler(self, event_type):

        def decorator(func):
            if event_type in self.handlers:
                self.handlers[event_type].append(func)
            else:
                self.handlers[event_type] = [func]
            return func

        return decorator

    def comment_handler(self):
        return self.custom_handler("video_comment_new")

    def question_handler(self):
        return self.custom_handler("sq_question")

    def friend_answer_handler(self):
        return self.custom_handler("sq_friend_answer")

    def right_answer_handler(self):
        return self.custom_handler("sq_question_answers_right")

    def end_game_handler(self):
        return self.custom_handler("sq_ed_game")

    def start_game_handler(self):
        return self.custom_handler("__start_game")

    def game_winners_handler(self):
        return self.custom_handler("sq_game_winners")

    def all_events_handler(self):
        return self.custom_handler("__all__")

    def last_time_answer_handler(self):
        return self.custom_handler("last_time_answer")
