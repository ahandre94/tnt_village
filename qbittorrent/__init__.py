import requests
from distutils.version import LooseVersion


def init_qb(address='127.0.0.1', port=8080):
    url = f'http://{address}:{port}'

    r = requests.get(f'{url}/version/qbittorrent')
    version = r.text
    if version and LooseVersion('v3.2.0') < LooseVersion(version) < LooseVersion('v4.0.4'):
        from .qb_previous import QbPrevious
        return QbPrevious(address, port)

    r = requests.get(f'{url}/api/v2/app/version')
    version = r.text
    if LooseVersion(version) > LooseVersion('v4.1'):
        from .qb_current import QbCurrent
        return QbCurrent(address, port)

    raise ValueError('Versione di qBittorrent non supportata')
