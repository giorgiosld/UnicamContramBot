#importo telegram API
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, CallbackContext
from telegram.ext import MessageHandler, Filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
import logging
#importo selenium API
import sys
from selenium import webdriver as wd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#importo libreria per i regex
import re
#importo librerie per lavorare con il pdf
import os
import glob

#funzione invio pdf sul canale del bot
def sendPdf(update, context):
    home = os.environ['HOME']
    nameHome = home[6:]
    list_of_files = glob.glob('/home/'+nameHome+'/Downloads/*.pdf')
    latest_file = max(list_of_files, key=os.path.getctime)
    context.bot.send_document(chat_id=update.effective_chat.id, document=open(latest_file, 'rb'), filename='bigliettoContram.pdf')

#funzione errore prenotazione
def userNotRegistered(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Utente non registrato nel sistema. Premere /help o inserire tramite /insert!")

#funzione prenotazione contram
def contram(info, update, context):
    #lettura dati linea di comando
    andata = info[0]
    ritorno = info[1]
    day = info[2]
    user = info[3]

    #lettura dati passeggero
    with open('datiPasseggero.txt', 'r') as f:
        user = user + "\n"
        for line in f:
            if(line == user):
                emailPass = f.readline()
                nomePass = f.readline()
                cognomePass = f.readline()
                uniPass = f.readline()
                phonePass = f.readline()	
            #possibile bug fare ulteriori check con piu utenti nel sistema	
            elif not line:
                userNotRegistered(update, context)
                return None

    #starting bot
    home = os.environ['HOME']
    nameHome = home[6:]
    profile = wd.FirefoxProfile()
    profile.set_preference("browser.download.folderList",2)
    profile.set_preference("browser.download.manager.useWindow", False)
    profile.set_preference("browser.download.dir", "/home/"+nameHome+"/Downloads")    
    profile.set_preference("browser.helperApps.neverAsk.saveToDisk", "application/pdf, application/force-download")
    profile.set_preference("dom.disable_beforeunload", True)
    profile.set_preference("pdfjs.disabled", True)
    
    browser = wd.Firefox(firefox_profile=profile)
    browser.implicitly_wait(2)

    browser.get("https://marcheroma.contram.it/home/index")

    #chiusura banner cookies
    try:
        cookie = WebDriverWait(browser, 5).until(
            EC.element_to_be_clickable((By.CLASS_NAME, "cc-compliance"))
        )
    finally:
        cookie.click()

    #inserimento partenza/arrivo form
    partenza = browser.find_element_by_xpath('//*[@id="input-partenza-flexdatalist"]')
    partenza.send_keys(andata)
    inizio = browser.find_element_by_xpath('/html/body/ul/li/span/span')
    inizio.click()

    browser.implicitly_wait(2)

    arrivo = browser.find_element_by_xpath('//*[@id="input-destinazione-flexdatalist"]')
    arrivo.send_keys(ritorno)
    fine = browser.find_element_by_xpath('/html/body/ul/li/span/span')
    fine.click()


    #inserimento data viaggio form
    data = browser.find_element_by_xpath('//*[@id="input-data-andata"]').clear()
    date = browser.find_element_by_xpath('//*[@id="input-data-andata"]')
    date.send_keys(day)

    #selezione studente unicam
    viaggiatore = browser.find_element_by_xpath('//*[@id="input-passeggeri"]')
    viaggiatore.click()
    adulti = browser.find_element_by_xpath('/html/body/div[2]/div[2]/form/div/div[5]/div/div[1]/div/div/button[1]/i')
    adulti.click()
    unicam = browser.find_element_by_xpath('/html/body/div[2]/div[2]/form/div/div[5]/div/div[3]/div/div/button[2]/i')
    unicam.click()

    search = browser.find_element_by_xpath('/html/body/div[2]/div[2]/form/div/div[6]/button')
    search.click()

    #inizio prenotazione
    prenota = browser.find_element_by_xpath('/html/body/div[2]/div[3]/div/div/table/tbody/tr/td[4]/form/button')
    prenota.click()

    confirm = browser.find_element_by_xpath('/html/body/div[2]/div[4]/div/div[2]/form/button')
    confirm.click()

    #inserimento dati passeggero
    email = browser.find_element_by_xpath('/html/body/div[2]/form/div/div[1]/div/input')
    email.send_keys(emailPass)

    nome = browser.find_element_by_xpath('/html/body/div[2]/form/div/div[3]/div[1]/div/input')
    nome.send_keys(nomePass)

    cognome = browser.find_element_by_xpath('/html/body/div[2]/form/div/div[3]/div[2]/div/input')
    cognome.send_keys(cognomePass)

    emailUnicam = browser.find_element_by_xpath('/html/body/div[2]/form/div/div[3]/div[3]/div/input')
    emailUnicam.send_keys(uniPass)

    telefono = browser.find_element_by_xpath('/html/body/div[2]/form/div/div[3]/div[4]/div/input')
    telefono.send_keys(phonePass)

    complete = browser.find_element_by_xpath('/html/body/div[2]/form/div/button')
    complete.click()

    browser.implicitly_wait(2)


    #conferma acquisto
    confirm = browser.find_element_by_xpath('//*[@id="btn-pagamento"]')
    confirm.click()

    browser.implicitly_wait(2)

    #pdf download
    pdf = browser.find_element_by_xpath('/html/body/div[2]/div[1]/div/div/form/div[2]/div[2]/button/span')
    pdf.click()

    browser.implicitly_wait(10)
    browser.close()
    info.clear()
    sendPdf(update, context)

#funzione controllo regex
def reg(campo):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, campo)):
        return True
    else:
        return False

#funzione per lo start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot per prenotare corriera contram /help ")

#malfunionamento query.data capire cosa arriva di vari bottoni
def button(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if(query.data == '2'):
        query.answer()
        query.edit_message_text(text=f"Per favore inserisci nuovamente i dati in maniera corretta")
    elif(query.data == '1'):
        query.answer()
        query.edit_message_text(text=f"Prenotazione in corso.. controllare email per vedere se bot funziona correttamente")
        contram(info, update, context)
    else:
        query.answer()
        query.edit_message_text(text=f"I tuoi dati saranno inseriti nel nostro sistema")
        with open("datiPasseggero.txt", "a") as f:
            f.write(str(update.effective_chat.id)+"\n")
            f.write(dataUsers[0]+"\n"+dataUsers[1]+"\n"+dataUsers[2]+"\n"+dataUsers[3]+"\n"+dataUsers[4]+"\n")
        dataUsers.clear()	

def caps(update, context):
    text_caps = ' '.join(context.args).upper()
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_caps)

#in caso di /caps con msg vuoto causerà un telegram.error.BadRequest: Message text is empty
def help(update, context):
    text_help = '''/start per iniziare a interagire con il bot
/caps <qualcosa> te lo trasforma in maiuscolo
/book <partenza> <arrivo> <dataViaggio> prenota il biglietto alla contram
/insert <emailToReceive> <Name> <Surname> <unicamMail> <numPhone> inserisce utente nel sistema
/display mostra dati utente
'''
    context.bot.send_message(chat_id=update.effective_chat.id, text=text_help)

def prenota(update, context):
    if (len(context.args) != 3):
        error_message = '''Immisione campi errata. Per favore specificare città partenza, città arrivo e la data usando il seguente formato:
    /book <cittàPartenza> <cittàArrivo> <dataViaggio>'''
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)
        return None

    partenza, arrivo, dataViaggio = context.args[0], context.args[1], context.args[2]
    response_msg = "Partenza: "+partenza+"\nArrivo: "+arrivo+"\nData del viaggio: "+dataViaggio

    context.bot.send_message(chat_id=update.effective_chat.id, text=response_msg)
    keyboard_book = [
        [
            InlineKeyboardButton("Si", callback_data='1'),
            InlineKeyboardButton("No", callback_data='2'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard_book)
    update.message.reply_text('I dati inseriti sono corretti?', reply_markup=reply_markup)

    info.append(partenza)
    info.append(arrivo)
    info.append(dataViaggio)
    info.append(str(update.effective_chat.id))

def insertUser(update, context):
    if(len(context.args) != 5):
        error_message = '''Immisione campi errata. Per favore specificare indirizzo dove ricevere email, nome, cognome, emailUnicam e il numero di telefono usando il seguente formato:
    /insert <emailToReceive> <Name> <Surname> <unicamMail> <numPhone>'''
        context.bot.send_message(chat_id=update.effective_chat.id, text=error_message)
        return None
    email, nome, cognome, uniMail, phoneNum = context.args[0], context.args[1], context.args[2], context.args[3], context.args[4]

    #check data inseriti da user
    if(reg(email) == False or reg(uniMail) == False):
        regexMail_error_message = "L'utente ha inserito un email non valida"
        context.bot.send_message(chat_id=update.effective_chat.id, text=regexMail_error_message)
        return None
    if(not phoneNum.isdigit() or len(phoneNum)!=10):
        phone_error_message = "L'utente ha inserito un numero di telefono non valido"
        context.bot.send_message(chat_id=update.effective_chat.id, text=phone_error_message)
        return None

    response_msg = "Email: "+email+"\nNome: "+nome+"\nCognome: "+cognome+"\nEmail unicam: "+uniMail+"\nNumero di telefono: "+phoneNum
    with open("datiPasseggero.txt", "r") as f:
        check = str(update.effective_chat.id)
        check = check+"\n"
        for line in f:
            #civitanova marche solo una parola eseguire eccezione per questa località
            #non manda ultimo pdf in memoria ma penultimo non relativo all'acquisto del cliente
            #print('line '+line+str(len(line)))
            #print('user '+check+str(len(check)))
            if(line == check):
                presence_error_message = "L'utente proprietario della chat ha già i dati inseriti nel nostro sistema. Per favore evitate stronzate!"
                context.bot.send_message(chat_id=update.effective_chat.id, text=presence_error_message)
                return None

    dataUsers.append(email)
    dataUsers.append(nome)
    dataUsers.append(cognome)
    dataUsers.append(uniMail)
    dataUsers.append(phoneNum)

    context.bot.send_message(chat_id=update.effective_chat.id, text=response_msg)
    keyboard_insert = [
        [
            InlineKeyboardButton("Si", callback_data='3'),
            InlineKeyboardButton("No", callback_data='2'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard_insert)
    update.message.reply_text('I dati inseriti sono corretti?', reply_markup=reply_markup)

def displayUser(update, context):
    with open('datiPasseggero.txt', 'r') as f:
        user = str(update.effective_chat.id)
        user = user +"\n"
        for line in f:
            if(line == user):
                emailPass = f.readline()
                nomePass = f.readline()
                cognomePass = f.readline()
                uniPass = f.readline()
                phonePass = f.readline()
                context.bot.send_message(chat_id=update.effective_chat.id, text="Email: "+emailPass+"Nome: "+nomePass+"Cognome: "+cognomePass+"Email unicam: "+uniPass+"Numero di telefono: "+phonePass)	
                return None
        userNotRegistered(update, context)
        return None



def main() -> None:
    #creazione updater con inserimento tokenBot
    updater = Updater(token = '1955397203:AAGXlnrGjJHyKt10uIRXDyST3Zp1fqCd9ls', use_context = True)
    #creazione dispatcher
    dispatcher = updater.dispatcher
    #in caso di errori una logError
    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

    #variabile globale contenente lista con dati viaggio e dati utenti
    global dataUsers
    global info
    info = []
    dataUsers = []

    #creazione del comando e inserimento sul bot
    start_handler = CommandHandler('start', start)
    dispatcher.add_handler(start_handler)

    #necesarrio per risolvere le callback riguardanti il prenota
    updater.dispatcher.add_handler(CallbackQueryHandler(button))

    caps_handler = CommandHandler('caps', caps)
    dispatcher.add_handler(caps_handler)

    help_handler = CommandHandler('help', help)
    dispatcher.add_handler(help_handler)

    book_handler = CommandHandler('book', prenota)
    dispatcher.add_handler(book_handler)

    insert_handler = CommandHandler('insert', insertUser)
    dispatcher.add_handler(insert_handler)

    display_handler = CommandHandler('display', displayUser)
    dispatcher.add_handler(display_handler)

    #avvio funzioni bot
    updater.start_polling()

    #spegnimento bot script
    updater.idle()

if __name__ == '__main__':
    main()
