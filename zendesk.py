import requests
import json
import time

class ZendeskClient():
    def __init__(self):
        self.__request = requests.Session()
        self.__request.auth = self.__auth
    
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