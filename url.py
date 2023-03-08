# -*- coding: utf-8 -*-
import configparser
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import time
#  Url oluşturan ve liste döndüren kısım
class Url:      
    def url_cek(self,sayfa):

        config = configparser.ConfigParser()
        config.read('filtre.ini', encoding='utf-8')
    

        araba_dict = {}

        renkKodlari = {"BEYAZ": "33611", "SİYAH": "33616", "GRİ": "33612", "LACİVERT": "33615", "KIRMIZI": "33613", "TURUNCU": "40148", "YEŞİL": "33618", "MAVİ": "33610", "BORDO": "33617", "KAHVERENGİ": "33621", "FÜME": "658878", "ŞAMPANYA": "675106", "SARI": "33614", "MOR": "33624", "TURKUAZ": "44926", "PEMBE": "40167", "GÜMÜŞ GRİ": "40948", "BEJ": "655354"}


        for section in config.sections():
            for key, value in config.items(section):
                araba_dict[key] = value
        renkKodu = renkKodlari.get(araba_dict["renk"].upper(), "")

        url = "https://www.sahibinden.com/"+ araba_dict["model"] +"?pagingOffset="+str(sayfa)+"&a3=" +renkKodu+ "&a5_max="+ araba_dict["max_year"]+"&a4_max="+araba_dict["max_km"]+"&sorting=price_asc&a4_min="+araba_dict["min_km"]+"&a5_min="+ araba_dict["min_year"]+"&price_min="+araba_dict["min_price"]+"&price_max"+araba_dict["max_price"]
        print('*******************************************************************************')
        print(url)
        print('*******************************************************************************')
        headers = {
            'User-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36'
        }
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
        
        return lists