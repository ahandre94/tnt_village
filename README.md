# TNTVillage
Cerca tra le release di TNTVillage, recupera il magnet del file che desideri e sfrutta l'integrazione con qBittorrent.
Sfrutta il bot Telegram per semplificare la ricerca @tntvillage_qb_bot


### Ricerca
Inserisci tra virgolette il nome del file che vuoi cercare

```console
$ python3 tnt.py -s 'prova'

TOPIC    HASH    TITOLO    DESCRIZIONE    DIMENSIONE
1        hash1   Prova     Descrizione    1.20 GB
2        hash2   Prova 2   Descr. 2       4.20 GB
```


### Download
Per effettuare un download basta utilizzare il topic che si è trovato dopo la fase di ricerca (per fare più download separare con uno spazio i topic)

```console
$ python3 tnt.py -d 1

magnet:?xt=urn:btih:...
```

```console
$ python3 tnt.py -d 1 2

magnet:?xt=urn:btih:1...
magnet:?xt=urn:btih:2...
```
Ed ecco il magnet da utilizzare

### qBittorrent
Per scaricare direttamente utilizzando qBittorrent, attivare l'interfaccia web (Preferenze -> Interfaccia web). È supportata sia la versione corrente (v4.1+) che la precedente (v3.2.0 - v4.0.4)

```console
$ python3 tnt.py -d 1 -qb -u 'admin' -pw 'adminadmin' -a '127.0.0.1' -p 8080
```

Di default l'username è `admin`, la password `adminadmin`, l'indirizzo IP `127.0.0.1` e la porta utilizzata `8080`. Se le tue credenziali sono queste, ti basterà passare come argomento solo qb

```console
$ python3 tnt.py -d 1 -qb
```
### Telegram
link: https://t.me/tntvillage_qb_bot

Una volta avviato il bot con
```/start```
puoi fare una ricerca utilizzando
```/search CONTENUTO DA CERCARE```,
fare un download copiando sempre il topic del file
```/download TOPIC```
e inizializzare qBittorrent con
```/init_qb```.
In questo caso non è possibile utilizzare un indirizzo locale per accedere all'interfaccia web
