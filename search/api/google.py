import requests
import os


class GoogleMap:
    url = "https://maps.googleapis.com/maps/api/geocode/json"

    def __init__(self, cordinates, key=None):
        if not key:
            key = os.getenv('google_maps_key')
        self.key = key
        self.cordinates = cordinates
        # Hold the raw response
        self.response = None
        # Hold the response code
        self.response_code = None
        # Hold the errors
        self.error = None
        # Hold the actual result set of a query
        self.results = None

    def work(self):
        # Literally just turns a tuple into a comma separated string of
        # latitude,longitude
        data = {
            "latlng": ",".join(map(str, self.cordinates)),
            "key": self.key
        }
        self.response = requests.get(self.url, data).json()
        self.__validate__()

    def __validate__(self):
        status = self.response['status']
        if status == 'OK':
            self.results = self.response['results']
        elif status == 'ZERO_RESULTS':
            self.error = 'zero results'
        else:
            self.error = self.response['error_message']

    def is_okay(self):
        return False if self.error else True

    def get_error(self):
        return self.error

    def get_results(self):
        return self.results
