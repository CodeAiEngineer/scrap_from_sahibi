# -*- coding: utf-8 -*-
# Url sayfasından veri çekme
class AracCek:
    def aracCek(self,lists, toplamListelenenAracSayisi,aracListesi):
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
                
        print('*******************************************************************************')    
        print("Founded "+str(toplamListelenenAracSayisi)+" advert(s)")    
        print('*******************************************************************************')
        return aracListesi, toplamListelenenAracSayisi       
            