from .qb import Qb


class QbCurrent(Qb):
    """qBittorent wrapper for qBittorrent v4.1+"""

    def __init__(self, address='127.0.0.1', port=8080):
        super().__init__(address, port)
        self.url = f'{self.url}/api/v2'

    def login(self, username='admin', password='adminadmin'):
        data = {'username': username, 'password': password}
        r = self.session.post(f'{self.url}/auth/login', data=data)
        return r.text == 'Ok.'

    def logout(self):
        r = self.session.post(f'{self.url}/auth/logout')

    def download_from_link(self, link):
        if isinstance(link, list):
            link = '\n'.join(link)
        data = {'urls': link}
        r = self.session.post(f'{self.url}/torrents/add', data=data)
        return r.text == 'Ok.'
