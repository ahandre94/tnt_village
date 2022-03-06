import os
import logging

from dotenv import load_dotenv
load_dotenv()

from telegram import Update, ParseMode, ReplyKeyboardRemove
from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    ConversationHandler,
    CallbackContext,
    Filters
)

from tnt import search, retrieve_magnet
from qbittorrent import init_qb


logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()


mode = os.getenv('MODE', 'development')
TOKEN = os.getenv('TOKEN')
ADDRESS, PORT, USERNAME, PASSWORD = range(4)

global qb
qb = None


def start_callback(update: Update, _: CallbackContext):
    logger.info('User {} started bot'.format(update.effective_user['id']))
    update.message.reply_text(
        'Cosa puoi fare con questo bot? '
        '<b>Cercare</b> nel database di TNTVillage quello che desideri scaricare con'
        '\n/search CONTENUTO DA CERCARE'
        '\ne una volta trovato quello che vuoi scaricare, fare il download del '
        '<b>magnet</b> copiando il topic del file'
        '\n/download TOPIC'
        '\nSe utilizzi <b>qBittorrent</b>, inizializzalo con /init_qb e quando '
        'scaricherai i contenuti con /download li vedrai direttamente in qBit. '
        'Per controllare i dati inseriti in fase di inizializzazione usa il comando /qbit',
        parse_mode=ParseMode.HTML
    )


def search_callback(update: Update, context: CallbackContext):
    query = ' '.join(context.args)
    logger.info('User {} searched for {}'.format(update.effective_user['id'], query))
    result = search(query)
    headers=['TOPIC', 'HASH', 'TITOLO', 'DESCRIZIONE', 'DIMENSIONE']
    if result:
        for res in result:
            msg = ''
            for field, header in zip(res, headers):
                msg += f'<b>{header}</b>: {field}\n'
            update.message.reply_text(msg, parse_mode=ParseMode.HTML)
    else:
        update.message.reply_text('Contenuto non trovato')


def download_callback(update: Update, context: CallbackContext):
    global qb
    if qb is None:
        init_qbittorrent(update, context)

    topic = context.args
    logger.info('User {} downloaded {}'.format(update.effective_user['id'], topic))
    for t in topic:
        link = retrieve_magnet(t)
        update.message.reply_text(link)
        if qb is not None:
            qb.download_from_link(link)


def qbit_callback(update: Update, context: CallbackContext):
    address, port, username, password = _get_qbit_info(context)

    if address and port and username and password:
        update.message.reply_text(
            f'<b>INDIRIZZO</b>: {address}'
            f'\n<b>PORTA</b>: {port}'
            f'\n<b>USERNAME</b>: {username}'
            f'\n<b>PASSWORD</b>: {password}',
            parse_mode=ParseMode.HTML
        )


def start_qb(update: Update, _: CallbackContext):
    logger.info('User {} started qBittorrent initializion'.format(update.effective_user['id']))
    update.message.reply_text(
        'Inizializza qBittorrent. Per prima cosa inserisci l\'indirizzo IP. '
        'Invia /cancel se vuoi stoppare il processo'
    )
    return ADDRESS


def address(update: Update, context: CallbackContext):
    user = update.message.from_user
    context.user_data['address'] = update.message.text
    update.message.reply_text(
        'Ora inserisci la porta'
    )
    return PORT


def port(update: Update, context: CallbackContext):
    user = update.message.from_user
    try:
        context.user_data['port'] = int(update.message.text)
    except:
        context.user_data['port'] = 8080
    update.message.reply_text(
        'Ora inserisci il tuo username'
    )
    return USERNAME


def username(update: Update, context: CallbackContext):
    user = update.message.from_user
    context.user_data['username'] = update.message.text
    update.message.reply_text(
        'Ora inserisci la password'
    )
    return PASSWORD


def password(update: Update, context: CallbackContext):
    user = update.message.from_user
    context.user_data['password'] = update.message.text
    update.message.reply_text(
        'Per controllare che i dati inseriti siano corretti usa /qbit altrimenti reimpostali con /init_qb'
    )
    return ConversationHandler.END


def cancel(update: Update, _: CallbackContext):
    user = update.message.from_user
    logger.info('User {} canceled qBittorrent initializion'.format(update.effective_user['id']))
    update.message.reply_text('Bye!', reply_markup=ReplyKeyboardRemove())
    return ConversationHandler.END


def _get_qbit_info(context: CallbackContext):
    address = context.user_data.get('address')
    port = context.user_data.get('port')
    username = context.user_data.get('username')
    password = context.user_data.get('password')
    return address, port, username, password


def init_qbittorrent(update: Update, context: CallbackContext):
    global qb

    address, port, username, password = _get_qbit_info(context)

    if address and port and username and password:
        try:
            qb = init_qb(username, password, address, port)
            log = qb.login(username, password)
            if not log:
                qb = None
                update.message.reply_text('Credenziali errate')
            else:
                update.message.reply_text('qBittorrent inizializzato')
                logger.info('User {} initialized qbittorrent'.format(update.effective_user['id']))
        except Exception as e:
            logger.info('exception {}'.format(e))
            qb = None
            update.message.reply_text('Avvia qBittorrent prima!')


def error_handler(update: Update, context: CallbackContext):
    logger.error(msg='Exception while handling an update:', exc_info=context.error)
    raise


if mode == 'development':
    def run(updater):
        updater.start_polling()
        updater.idle()
elif mode == 'production':
    def run(updater):
        PORT = int(os.environ.get('PORT', '8443'))
        HEROKU_APP_NAME = os.environ.get('HEROKU_APP_NAME')
        updater.start_webhook(
            listen='0.0.0.0',
            port=PORT,
            url_path=TOKEN,
            webhook_url=f'https://{HEROKU_APP_NAME}.herokuapp.com/{TOKEN}'
        )
else:
    raise ValueError('Mode not supported')


def main():
    updater = Updater(TOKEN)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start_callback))
    dispatcher.add_handler(CommandHandler('search', search_callback))
    dispatcher.add_handler(CommandHandler('download', download_callback))
    dispatcher.add_handler(CommandHandler('qbit', qbit_callback))

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('init_qb', start_qb)],
        states={
            ADDRESS: [MessageHandler(Filters.text, address)],
            PORT: [MessageHandler(Filters.text, port)],
            USERNAME: [MessageHandler(Filters.text, username)],
            PASSWORD: [MessageHandler(Filters.text, password)]
        },
        fallbacks=[CommandHandler('cancel', cancel)],
    )
    dispatcher.add_handler(conv_handler)

    dispatcher.add_error_handler(error_handler)

    run(updater)


if __name__ == '__main__':
    main()
