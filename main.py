import requests as r
from bs4 import BeautifulSoup as bs

from sender import send_email

from dotenv import load_dotenv
import os
from os.path import join, dirname

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

port = os.environ.get("PORT")
smtp_server = os.environ.get("SMTP_SERVER")
sender_email = os.environ.get("SENDER_EMAIL")
password = os.environ.get("PASSWORD")
email = os.environ.get("RECEIVER_EMAIL")
path_to_file = os.environ.get("VENUES")

url = "https://lidovajidelna.cz"

def get(url):
    page = r.get(url)
    return page

def soup(page):
    return bs(page.content, 'html.parser')

def main():
    lidovka = soup(get(url))
    Food_items = lidovka.find_all("td")
    for item in Food_items:
        value = item.find("p").text.strip()
        if value == "Espresso":
            break
        if value == "":
            continue
        print(value)
        
        if ("segedín" in value.lower() or "segedin" in value.lower()) and "soj" in value.lower(): 
            sender()

def sender():
    subject = "SOJOVÝ SEGEDÍN ALERT!"
    text = "Ahoj E.,\n\n Mám pro tebe dobrou zprávu! SOJOVÝ SEGEDÍN JE V NABÍDCE. Pro jistotu si to zkontroluj na https://lidovajidelna.cz a naplánuj si cestu za dobrůtkou!"
    message = f"From: {sender_email}\r\nTo: {email}\r\nSubject:{subject}\r\n{text}"
    send_email(port, smtp_server, sender_email, password, email, message)            
        
if __name__ == '__main__':
    main() 
