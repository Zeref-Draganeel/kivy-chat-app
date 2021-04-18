import requests

BASE_URL = 'http://127.0.0.1:5000/'

class Client:
    token = None

    def post(self, endpoint, data):
        return requests.post(BASE_URL + endpoint, json = data)

    def get(self, endpoint, data):
        return requests.get(BASE_URL + endpoint, json = data).json()
