# -*- coding: utf-8 -*-
import configparser
import subprocess
import os
from flask import Flask
import time

app = Flask(__name__)

@app.route('/filter')

class UserInput:
    def __init__(self):
        self.config = configparser.ConfigParser()
        self.config.read('filtre.ini', encoding='utf-8')

    def run(self):
        if 'ARABA' not in self.config:
            self.config['ARABA'] = {}
        self.config['ARABA']['model'] = input('Model: ')
        self.config['ARABA']['min_year'] = input('Minimum yıl: ')
        self.config['ARABA']['max_year'] = input('Maksimum yıl: ')
        self.config['ARABA']['min_price'] = input('Minimum fiyat: ')
        self.config['ARABA']['max_price'] = input('Maksimum fiyat: ')
        self.config['ARABA']['min_km'] = input('Minimum km: ')
        self.config['ARABA']['max_km'] = input('Maksimum km: ')
        self.config['ARABA']['renk'] = input('Renk: ')
        with open('filtre.ini', 'w', encoding='utf-8') as configfile:
            self.config.write(configfile)
        print('Veri başarılı bir şekilde filtrelendi')

                
    
    # Docker olmadan calismasi icin
    
    #@app.route('/filter', methods=['POST'])
    # def filterData():
    #     userInput = UserInput()
    #     userInput.run()
    #     main = ArabaFiltresi()
    #     main.run()
        
userInput = UserInput()
userInput.run()
#UserInput.filterData()


build_command = 'docker build -t scrap_from_sahibi .'
subprocess.run(build_command, shell=True)

run_command = 'docker run -p 9999:9999 -it scrap_from_sahibi'
process = subprocess.Popen(run_command, shell=True)

time.sleep(1.5)
command = 'telnet 127.0.0.1 9999'
os.system(command)

