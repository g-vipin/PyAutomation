import requests
class ApiClient:
    def __init__(self):
        self.response = requests.get("https://www.python.org")