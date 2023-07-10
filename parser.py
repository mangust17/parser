import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils.dataframe import dataframe_to_rows

URL_TEMPLATE = "https://career.avito.com/vacancies/?q=&action=filter&direction=5"
FILE_NAME = "test.xlsx"


def parse(url=URL_TEMPLATE):
    result_list = {'Ссылка': [], 'Название': [], 'Место работы': []}
    r = requests.get(url)
    soup = bs(r.text, "html.parser")
    vacancies_info = soup.find_all('a', class_='vacancies-section__item-link')
    for info in vacancies_info:
        result_list['Ссылка'].append('https://career.avito.com/vacancies/razrabotka/' + info['data-vacancy-id'] + '/')
        result_list['Название'].append(info.find('span', class_='vacancies-section__item-name').text)
        result_list['Место работы'].append(info.find('span', class_='vacancies-section__item-meta').text)
    return result_list


df = pd.DataFrame(data=parse())
wb = Workbook()
ws = wb.active
ws.title = "Sheet1"
for row in dataframe_to_rows(df, index=False, header=True):
    ws.append(row)

ws.sheet_view.tabSelected = True
wb.save(FILE_NAME)
