import requests
from distutils.version import LooseVersion


def init_qb(username='admin', password='adminadmin', address='127.0.0.1', port=8080):
    url = f'http://{address}:{port}'

    try:
        r = requests.get(f'{url}/version/qbittorrent')
        version = r.text
        if version and LooseVersion('v3.2.0') <= LooseVersion(version) <= LooseVersion('v4.0.4'):
            from .qb_previous import QbPrevious
            return QbPrevious(address, port)
    except:
        pass

    try:
        data = {'username': username, 'password': password}
        r = requests.post(f'{url}/api/v2/auth/login', data=data)
        sid = r.cookies['SID']
        headers={'Cookie': f'SID={sid}'}
        r = requests.get(f'{url}/api/v2/app/version', headers=headers)
        version = r.text
        if version and LooseVersion(version) >= LooseVersion('v4.1'):
            from .qb_current import QbCurrent
            return QbCurrent(address, port)
    except:
        pass

    raise ValueError('Versione di qBittorrent non supportata')
