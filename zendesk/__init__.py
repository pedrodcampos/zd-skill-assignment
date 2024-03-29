import requests
import json
import time

class ZendeskClient():
    def __init__(self):
        config = json.load(open("config.json"))
        self.__request = requests.Session()
        self.url = config.get("url",None)
        self.__request.auth = (config.get("user",None), config.get("password",None))
    
    def get(self,endpoint, **kwargs):
        response = None
        while response is None:
            response = self.__request.get(self.url+endpoint, **kwargs)
            if response.status_code == 429:
                wait_time = int(response.headers.get('Retry-After',60))
                time.sleep(wait_time)
                response = None
                continue
        return response.json()

    def post(self, endpoint, **kwargs):
        return self.__request.post(self.url+endpoint, **kwargs)