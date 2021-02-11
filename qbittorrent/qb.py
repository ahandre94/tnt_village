import requests


class Qb:
    def __init__(self, address='127.0.0.1', port=8080):
        self.url = f'http://{address}:{port}'
        self.session = requests.Session()

    def login(self, username, password):
        raise NotImplementedError

    def logout(self):
        raise NotImplementedError

    def download_from_link(self, link):
        raise NotImplementedError
