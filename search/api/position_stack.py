import requests
import os


class PositionStack:
    url = "http://api.positionstack.com/v1/reverse"

    def __init__(self, cordinates, key=None):
        if not key:
            key = os.getenv('position_stack_key')
        self.key = key
        self.cordinates = cordinates
        self.response = None
        self.response_code = None
        self.error = None
        self.results = None

    def __validate__(self):
        if 'error' in self.response:
            # Parse error
            self.error = []
            for key in self.response['error']['context']:
                error_msg = self.response['error']['context'][key]['message']
                self.error.append(error_msg)
        else:
            self.results = self.response['data']

    def work(self):
        data = {
            "query": ",".join(map(str, self.cordinates)),
            "access_key": self.key
        }
        self.response = requests.get(self.url, data).json()
        self.__validate__()

    def is_okay(self):
        return False if self.error else True

    def get_results(self):
        return self.results

    def get_error(self):
        return ",".join(self.error)
