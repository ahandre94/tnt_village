import requests

from .qb import Qb


class QbCurrent(Qb):
    """qBittorent wrapper for qBittorrent v4.1+"""

    def __init__(self, address='127.0.0.1', port=8080):
        super().__init__(address, port)

    def login(self, username, password):
        pass

    def logout(self):
        pass

    def download_from_link(self, link):
        pass
