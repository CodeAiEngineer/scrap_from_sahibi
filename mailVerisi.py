# -*- coding: utf-8 -*-
# e-posta olarak gönderilecek veri
class MailVerisi:
    def mailVerisi(self,aracListesi,numarator):
        aracListesiStr = ""
        
        for numarator, arac in enumerate(aracListesi, start=numarator+1):
            aracListesiStr += f"{numarator}. Araç Bilgileri:\n"
            aracListesiStr += f"\tModel Adı: {arac['modelName']}\n"
            aracListesiStr += f"\tModel Detayları: {arac['modelDetails']}\n"
            aracListesiStr += f"\tYıl: {arac['year']}\n"
            aracListesiStr += f"\tKilometre: {arac['mileage']}\n"
            aracListesiStr += f"\tRenk: {arac['color']}\n"
            aracListesiStr += f"\tFiyat: {arac['price']}\n\n"
        return aracListesiStr,numarator    