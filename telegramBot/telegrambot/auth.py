import requests
import telebot
from bs4 import BeautifulSoup
import requests
from typing import List, Tuple


def get_page(id_user) -> str:
    url = '{domain}:{id_user}'.format(
        domain='https://isu.ifmo.ru/pls/apex/f?p=2143:PERSON:106933509959320::NO:RP:PID',
        id_user=id_user
    )
    response = requests.get(url)
    web_page = response.text

    return web_page


def get_id():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:45.0) Gecko/20100101 Firefox/45.0'}
    datas = {
        "p_t18": '285891',
        "p_t19": 'Me4nik12_'
    }
    url = 'https://isu.ifmo.ru/pls/apex/f?p=2437:7:{domain}:::::'.format(
        domain = 107282354899480
    )
    s = requests.Session()
    loging = s.post(url, headers = headers, data = datas)
    web_page = loging.text
    print(web_page)


    return web_page


def parse_id_of_user(web_page):
    soup = BeautifulSoup(web_page, "html5lib")
    headder = soup.find('li')
    return headder


if __name__ == '__main__':
    web_page = get_id()
    head_id = parse_id_of_user(web_page)
