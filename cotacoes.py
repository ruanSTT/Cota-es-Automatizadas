from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager .firefox import GeckoDriverManager
from selenium.webdriver.firefox.service import Service
from datetime import datetime
import pandas as pd
import os
import csv


options = webdriver.FirefoxOptions()
web = webdriver.Firefox(options=options)

currency_units = ["USD", "ARS", "GBP", "EUR", "BRL"]
date_hour = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
currency_data = []

for currency in currency_units:
    url = f'https://www.google.com/finance/quote/{currency}-BRL?sa=X&ved=2ahUKEwi{currency}'

    try:
        web.get(url)
    except Exception as e:
        print(f"Erro ao abrir a página para {currency}: {e}")
        continue

    xpath_price = '//div[@class="YMlKec fxKbKc"]'
    try:
        price_element = web.find_element(By.XPATH, xpath_price)
        price = price_element.text
    except Exception as e:
        print(f"Erro ao extrair a cotação para {currency}: {e}")
        continue

    currency_data.append({'date/hour': date_hour, 'currency': currency, 'price': price})

filename = os.path.join(os.getcwd(), 'cotacoes.csv')
if not os.path.exists(filename):
   
    header = ['Data e Hora', 'Moeda', 'Cotacao']
    with open(filename, 'w', newline='', encoding='utf-8',) as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow(header)

df = pd.DataFrame(currency_data)

df = df[['date/hour', 'currency', 'price']]

filename = os.path.join(os.getcwd(), 'cotacoes.csv')
df.to_csv(filename, mode='a', index=False, header=not os.path.exists(filename), sep=';')

print("The DataFrame was saved as cotacoes.csv")


web.quit()