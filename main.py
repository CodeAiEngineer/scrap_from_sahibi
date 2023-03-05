# -*- coding: utf-8 -*-

import configparser
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import time
from flask import Flask
from flask_mail import Mail
from flask_mail import Message
import time
import socket

renkKodlari = {"BEYAZ": "33611", "SİYAH": "33616", "GRİ": "33612", "LACİVERT": "33615", "KIRMIZI": "33613", "TURUNCU": "40148", "YEŞİL": "33618", "MAVİ": "33610", "BORDO": "33617", "KAHVERENGİ": "33621", "FÜME": "658878", "ŞAMPANYA": "675106", "SARI": "33614", "MOR": "33624", "TURKUAZ": "44926", "PEMBE": "40167", "GÜMÜŞ GRİ": "40948", "BEJ": "655354"}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("0.0.0.0", 9999))
server.listen()
while True:
    client, addr = server.accept()  
    print("Connection from", addr)
    client.send("You are connected!\n".encode())
    
    sayfaDevam = True
    config = configparser.ConfigParser()
    config.read('filtre.ini', encoding='utf-8')
    sayfa = 1
    
    araba_dict = {}
    for section in config.sections():
        for key, value in config.items(section):
            araba_dict[key] = value
    renkKodu = renkKodlari.get(araba_dict["renk"].upper(), "")


    def sayfaIleri(sayfaDevam):
        sayfa = 1
        iterasyonSayisi=0
        aracListesiStrEski = ""
        while sayfaDevam == True:
                     
            url = "https://www.sahibinden.com/"+ araba_dict["model"] +"?pagingOffset="+str(sayfa)+"&a3=" +renkKodu+ "&a5_max="+ araba_dict["max_year"]+"&a4_max="+araba_dict["max_km"]+"&sorting=price_asc&a4_min="+araba_dict["min_km"]+"&a5_min="+ araba_dict["min_year"]+"&price_min="+araba_dict["min_price"]+"&price_max"+araba_dict["max_price"]
            print(url)
            headers = {
                'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
            }

            print(url)

            retry_count = 3
            for i in range(retry_count):
                try:
                    req = Request(url, headers=headers)
                    with urlopen(req, timeout=10) as response:
                        page = response.read()
                    break
                except Exception as e:
                    print(e)
                    if i == retry_count - 1:
                        raise
                time.sleep(5)

            soup = BeautifulSoup(page, 'html.parser')
            lists = soup.find_all("tr", class_=["searchResultsItem", "searchResultsPromoHighlight", "searchResultsPromoBold","searchResultsPromoSuper","searchResultsFireSale"])

            def arac_cek(lists):
                global toplamListelenenAracSayisi
                toplamListelenenAracSayisi=0
                global aracListesi 
                aracListesi = []
                for list in lists:
                    if "classicNativeAd" not in list.get("class", []):
                        toplamListelenenAracSayisi += 1
                        aracDict = {}
                        aracDict["modelName"] = list.find('td', class_='searchResultsTagAttributeValue').get_text().strip()
                        aracDict["modelDetails"] = list.find_all('td', class_='searchResultsTagAttributeValue')[1].get_text().strip()
                        aracDict["year"] = list.find('td', class_='searchResultsAttributeValue').get_text().strip()
                        aracDict["mileage"] = list.find_all('td', class_='searchResultsAttributeValue')[1].get_text().strip()
                        aracDict["color"] = list.find_all('td', class_='searchResultsAttributeValue')[2].get_text().strip()
                        aracDict["price"] = list.find('td', class_='searchResultsPriceValue').find('span').get_text().strip()
                        aracListesi.append(aracDict)

            arac_cek(lists)
            
            print("Founded "+str(toplamListelenenAracSayisi)+" advert(s)")
            if toplamListelenenAracSayisi != 0:
                iterasyonSayisi += 1
        
                email = input("Gönderilecek e-posta adresini girin: \n")

                aracListesiStr = ""

                def send_email(aracListesi,email):
                    app = Flask(__name__)
                    app.config['MAIL_DEFAULT_SENDER'] = 'info@example.com'
                    app.config['MAIL_SERVER']='sandbox.smtp.mailtrap.io'
                    app.config['MAIL_PORT'] = 2525
                    app.config['MAIL_USERNAME'] = '764ae6773aefb8'
                    app.config['MAIL_PASSWORD'] = 'e19bd3886816ae'
                    app.config['AUTH'] = 'PLAIN'
                    app.config['MAIL_USE_TLS'] = True
                    app.config['MAIL_USE_SSL'] = False

                    mail = Mail(app)

                    with app.app_context():
                        message = Message('Başlık', recipients=[email])
                        message.body = str(aracListesi)
                        mail.send(message)

                for i, arac in enumerate(aracListesi, start=1):
                    aracListesiStr += f"{i}. Araç Bilgileri:\n"
                    aracListesiStr += f"\tModel Adı: {arac['modelName']}\n"
                    aracListesiStr += f"\tModel Detayları: {arac['modelDetails']}\n"
                    aracListesiStr += f"\tYıl: {arac['year']}\n"
                    aracListesiStr += f"\tKilometre: {arac['mileage']}\n"
                    aracListesiStr += f"\tRenk: {arac['color']}\n"
                    aracListesiStr += f"\tFiyat: {arac['price']}\n\n"
                    
                send_email(aracListesiStr, email)

                if aracListesiStr != aracListesiStrEski:
                    aracListesiStrEski = aracListesiStr
                else:
                    print("Son sayfaya ulaştınız")
                    sayfaDevam=False

                if toplamListelenenAracSayisi > 19:
                    devam = input(str(toplamListelenenAracSayisi)+" adet gönderdik. Diğer sayfayı gönderelim mi? Y/N: \n")
                    if devam=="Y" or devam=="y":
                        sayfaDevam=True
                        sayfa += 20
                
                    else:
                        print("İşlem Sonlanıyor")        
                        sayfaDevam=False
                    
                else:
                    if iterasyonSayisi != 0:
                        print("Başka araç bulunamadı. İşlem sonlanıyor.")
                        sayfaDevam = False
                    else:
                        print("Araç bulunamadı. Lütfen tekrar deneyin")
                        sayfaDevam = False             
    sayfaIleri(sayfaDevam=True)
    #client.close()
