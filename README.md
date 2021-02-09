# TNTVillage
Cerca tra le release di TNTVillage e recupera il magnet del file che desideri


### Ricerca
Inserisci tra virgolette il nome del file che vuoi cercare

```console
$ python3 tnt.py -s 'prova'

TOPIC    TITOLO    DESCRIZIONE    DIMENSIONE
1        Prova     Descrizione    1.20 GB
2        Prova 2   Descr. 2       4.20 GB
```


### Download
Per effettuare un download basta utilizzare il topic che si è trovato dopo la fase di ricerca (per fare più download separare con uno spazio i topic)

```console
$ python3 tnt.py -d 1

magnet:/?xt=urn:btih:...
```

```console
$ python3 tnt.py -d 1 2

magnet:/?xt=urn:btih:1...
magnet:/?xt=urn:btih:2...
```
Ed ecco il magnet da utilizzare
