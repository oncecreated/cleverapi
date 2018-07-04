import requests
import re
import urllib

class CleverAuth():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = requests.Session()
        self.url_access_allowed = None
        self.token = None

    def auth(self):
        csrf = self.__get_csrf()
        self.__login(csrf)

    def __get_csrf(self):
        url  = str("https://oauth.vk.com/authorize?client_id=6334949"
        "&scope=friends,video,notifications,notify,photos,wall,stories,"
        "groups,offline&redirect_uri=https://oauth.vk.com/blank.html&"
        "display=mobile&v=5.73&response_type=token&revoke=1")

        self.session.get(url)
        response = self.session.get(url).text
        
        csrf = dict()     
        pattern = r'<input type="hidden" name="(.+?.)" value="(.+?.)"(?:| /)>'

        for match in re.finditer(pattern, response):
            csrf[match.group(1)] = match.group(2)

        return csrf

    def __login(self, payload):
        url = "https://login.vk.com/?act=login&soft=1&utf8=1"
        
        payload["email"] = self.email
        payload["pass"] = self.password

        response = self.session.post(url, data=payload).text

        pattern = r'<form method="post" action="(.+?.)">'
        match = re.search(pattern, response)
        
        if match is not None:
            self.url_access_allowed = match.group(1)

    def get_token(self):
        if self.token is not None:
            self.token

        if self.url_access_allowed is None:
            raise Exception("self.url_access_allowed is None")

        response = self.session.post(self.url_access_allowed)
        self.token = response.url.split("#")[1].split("&")[0].split("=")[1]
        return self.token



