import requests

from .qb import Qb


class QbPrevious(Qb):
    """qBittorent wrapper for qBittorrent v3.2.0-v4.0.4"""

    def __init__(self, address='127.0.0.1', port=8080):
        super().__init__(address, port)
        self.SID = None

    def login(self, username='admin', password='adminadmin'):
        data = {'username': username, 'password': password}
        r = requests.post(f'{self.url}/login', data=data)
        if r.text == 'Ok.':
            cookies = r.cookies.get_dict()
            self.SID = cookies['SID']
            return True
        return False

    def logout(self):
        if self.SID is None:
            return False
        cookies = {'SID': self.SID}
        r = requests.post(f'{self.url}/logout', cookies=cookies)

    def download_from_link(self, link):
        if self.SID is None:
            print('Fai il login prima!')
            return False
        data = {'urls': link}
        cookies = {'SID': self.SID}
        r = requests.post(f'{self.url}/command/download', data=data, cookies=cookies)
        return r.text == 'Ok.'
