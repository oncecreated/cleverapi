import requests
import re
import urllib

class CleverAccount():
    def __init__(self, email, password):
        self.email = email
        self.password = password
        self.session = requests.Session()

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

        self.session.post(url, data=payload)

    def get_token(self):
        url = str("https://login.vk.com/?act=grant_access&client_id=6334949&"
        "settings=860247&redirect_uri=https%3A%2F%2Foauth.vk.com%2Fblank.html&"
        "response_type=token&group_ids=&token_type=0&v=5.73&state=&display=mobile&")

        response = self.session.post(url)
        token = response.url.split("#")[1].split("&")[0].split("=")[1]
        return token



