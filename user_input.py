# -*- coding: utf-8 -*-
from flask import Flask
import configparser
import subprocess
import os
app = Flask(__name__)

@app.route('/filter')
#@app.route('/filter', methods=['POST'])
def filter_data():
    get_input()
    return 'Data filtered successfully.'

def get_input():
    config = configparser.ConfigParser()
    config.read('filtre.ini', encoding='utf-8')
    if 'ARABA' not in config:
        config['ARABA'] = {}
    config['ARABA']['model'] = input('Model: ')
    config['ARABA']['min_year'] = input('Minimum yıl: ')
    config['ARABA']['max_year'] = input('Maksimum yıl: ')
    config['ARABA']['min_price'] = input('Minimum fiyat: ')
    config['ARABA']['max_price'] = input('Maksimum fiyat: ')
    config['ARABA']['min_km'] = input('Minimum km: ')
    config['ARABA']['max_km'] = input('Maksimum km: ')
    config['ARABA']['renk'] = input('Renk: ')
    with open('filtre.ini', 'w',encoding='utf-8') as configfile:
        config.write(configfile)
    print('Data filtered successfully.')
      
filter_data()

build_command = 'docker build -t scrap_from_sahibi .'
subprocess.run(build_command, shell=True)

run_command = 'docker run -p 9999:9999 -it scrap_from_sahibi'
process = subprocess.Popen(run_command, shell=True)

import time
time.sleep(0.5)
command = 'telnet 127.0.0.1 9999'
os.system(command)

