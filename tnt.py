import sys
import argparse
import csv
import requests

from bs4 import BeautifulSoup


TNT_DUMP = 'dump_release_tntvillage_2019-08-30.csv'
BASE_URL = 'https://web.archive.org/web/20200413084954/http://forum.tntvillage.scambioetico.org/index.php?showtopic='
UNIT = {0: 'B', 1: 'KB', 2: 'MB', 3: 'GB'}
CONV = 2**10


def parse_args():
	parser = argparse.ArgumentParser()
	parser.add_argument('-s', '--search', dest='search', type=str,
						help='Contenuto da cercare')
	parser.add_argument('-d', '--download', dest='download', nargs='+', type=int,
						help='Topic del file da scaricare')
	return parser.parse_args()


def _convert_dimension(dimension):
	c = 0
	while dimension > CONV:
		dimension /= CONV
		c += 1
	return f'{dimension:.2f} {UNIT[c]}'


def search(query):
	query = query.lower()
	res = []
	with open(TNT_DUMP) as f:
		r = csv.reader(f)
		fields = next(r)
		for elem in r:
			title = elem[fields.index('TITOLO')]
			description = elem[fields.index('DESCRIZIONE')]
			if query in title.lower() or query in description.lower():
				dimension = _convert_dimension(int(elem[fields.index('DIMENSIONE')]))
				res.append((elem[fields.index('TOPIC')], title, description, dimension))
	if res:
		res.sort(key=lambda item: (item[1].lower(), item[2].lower()))
		print(f'TOPIC\tTITOLO\tDESCRIZIONE\tDIMENSIONE')
		for topic, title, description, dimension in res:
			print(f'{topic}\t{title}\t{description}\t{dimension}')
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
			link = magnet[index:]
			print(link)
		except:
			print('Something went wrong')
	else:
		print('Topic non trovato')


if __name__ == '__main__':
	args = parse_args()

	if args.search:
		query = args.search
		search(query)

	if args.download:
		topic = args.download
		for t in topic:
			retrieve_magnet(t)
