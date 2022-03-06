from .qb import Qb


class QbPrevious(Qb):
    """qBittorent wrapper for qBittorrent v3.2.0-v4.0.4"""

    def __init__(self, address='127.0.0.1', port=8080):
        super().__init__(address, port)

    def login(self, username='admin', password='adminadmin'):
        data = {'username': username, 'password': password}
        r = self.session.post(f'{self.url}/login', data=data)
        return r.text == 'Ok.'

    def logout(self):
        r = self.session.post(f'{self.url}/logout')

    def download_from_link(self, link):
        if isinstance(link, list):
            link = '\n'.join(link)
        data = {'urls': link}
        r = self.session.post(f'{self.url}/command/download', data=data)
        return r.text == 'Ok.'
