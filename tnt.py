import sys
import argparse
import csv
import requests
from tabulate import tabulate

from bs4 import BeautifulSoup
from qbittorrent import init_qb


TNT_DUMP = 'dump_release_tntvillage_2019-08-30.csv'
BASE_URL = 'https://web.archive.org/web/20200413084954/http://forum.tntvillage.scambioetico.org/index.php?showtopic='
UNIT = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB'}


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--search', dest='search', type=str,
						help='Contenuto da cercare')
	parser.add_argument('-d', '--download', dest='download', nargs='+', type=int,
						help='Topic del file da scaricare')
	parser.add_argument('-qb', '--qbittorrent', dest='qb', action='store_true',
						help='Usa qBittorrent')
	parser.set_defaults(qb=False)
	parser.add_argument('-a', '--ip-address', dest='address', type=str,
						help='Indirizzo IP per accedere a qBittorrent (defualt: 127.0.0.1)')
	parser.set_defaults(address='127.0.0.1')
	parser.add_argument('-p', '--port', dest='port', type=int,
						help='Porta per accedere a qBittorrent  (defualt: 8080)')
	parser.set_defaults(port=8080)
	parser.add_argument('-u', '--username', dest='username', type=str,
						help='Username per accedere a qBittorrent (defualt: admin)')
	parser.set_defaults(username='admin')
	parser.add_argument('-pw', '--password', dest='password', type=str,
						help='Password per accedere a qBittorrent  (defualt: adminadmin)')
	parser.set_defaults(password='adminadmin')
	return parser.parse_args()


def _convert_dimension(dimension):
	CONV = 2**10
	c = 0
	while dimension > CONV:
		dimension /= CONV
		c += 1
	return f'{dimension:.2f} {UNIT[c]}'


def search(query):
	query = query.lower()
	if not query:
		return []

	res = []
	with open(TNT_DUMP, encoding='utf-8') as f:
		r = csv.reader(f)
		fields = next(r)
		for elem in r:
			title = elem[fields.index('TITOLO')]
			description = elem[fields.index('DESCRIZIONE')]
			if query in title.lower() or query in description.lower():
				topic = elem[fields.index('TOPIC')]
				hash = elem[fields.index('HASH')]
				dimension = _convert_dimension(int(elem[fields.index('DIMENSIONE')]))
				res.append((topic, hash, title, description, dimension))
	if res:
		res.sort(
			key=lambda item: (
				item[2].lower(),
				item[3].lower(),
				list(UNIT.keys())[list(UNIT.values()).index(item[4].split()[1])],
				item[4].split()[0],
				item[0],
				item[1]
			)
		)
	return res


def print_search_result(result):
	if result:
		print(tabulate(result, headers=['TOPIC', 'HASH', 'TITOLO', 'DESCRIZIONE', 'DIMENSIONE']))
	else:
		print('Contenuto non trovato')


def retrieve_magnet(topic):
	url = f'{BASE_URL}{topic}'
	r = requests.get(url)
	if r.status_code == 200:
		try:
			soup = BeautifulSoup(r.text, 'html.parser')
			table = soup.find_all('table', class_='tableborder')[1]
			magnet = table.find('a', title='Magnet link').get('href')
			index = magnet.find('magnet')
			magnet = magnet[index:]
			link = ''.join(magnet.split('/'))
			return link
		except:
			print('Something went wrong')
	return 'Topic non trovato'


if __name__ == '__main__':
	args = parse_args()

	if args.search:
		query = args.search
		result = search(query)
		print_search_result(result)

	if args.download:
		topic = args.download

		qb = None
		if args.qb:
			qb = init_qb(args.username, args.password, args.address, args.port)
			log = qb.login(args.username, args.password)
			if not log:
				print('Credenziali errate')
				sys.exit()

		for t in topic:
			link = retrieve_magnet(t)
			print(link)
			if qb is not None:
				qb.download_from_link(link)

		if qb is not None:
			qb.logout()
