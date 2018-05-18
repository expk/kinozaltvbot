import requests
from bs4 import BeautifulSoup

#import sys
import bencodepy
import hashlib
import base64

# url = http://kinozal.tv/browse.php

def get_html (url):
    r = requests.get(url)
    return r.text           # Возвращаем HTML - код страницы url


def get_all_links(html, maxsearch):
    # try:
    #     soup = BeautifulSoup(html, 'lxml')
    # except:
    #     print('Страница со списком найденных торрентов не загружена')
    #     exit(0)
    # try:
    #     tds = soup.find('table', class_='t_peer w100p').find_all('td', class_='nam')
    # except:
    #     print('По вашему запросу ничего не обнаружено')
    #     exit(0)
    soup = BeautifulSoup(html, 'lxml')
    # print(soup)
    tds = soup.find('table', class_='t_peer w100p').find_all('td', class_='nam')
    links = []

    # session = requests.session()                            # Авторизация
    # url_login = 'http://kinozal.tv/takelogin.php'           #
    # data = {'username': 'expk13', 'password': 'expk--'}     #
    # session.post(url_login, data=data).text                 #


    i = 0
    for td in tds:
        a = td.find('a').get('href')                                            # Строка с ссылками
        desc = td.find('a').text                                                # Описание торрента
        # link_torrent = get_page(session.post('http://kinozal.tv' + a).text)     # Получаем ссылку для скачивания
        link_torrent = 'http://dl.kinozal.tv/download.php?id=' + a.split ('=')[1]
        link = 'http://kinozal.tv' + a + ' ' + link_torrent + ' ' + desc        # Строка с ссылкой на страницу торрента, ссылка для скачивания и описание торрента

        links.append([a.split ('=')[1], desc])
        # print (len(links),'=',links)
        i += 1
        if i >= maxsearch:
            # print (i)
            break

        # if get_torrent_file(link_torrent, session) == 11:                                          # Скачать торрент файл во временный с именем 1.torrent
            # print(link)
            # link = link + ' ' + make_magnet_from_file('1.torrent')
            # print(link)
            # links.append(link)
            # i += 1
            # print ('i=',i)
            # if i == 5:
                # print (i)
                # break
        # else:
        #     i += 1
        #     link = link + ' ' + 'Не удалось скачать torrent файл'
            # print(link)
            # links.append(link)
            # print('Не удалось скачать torrent файл')
            # if i == 5:
                # print (i)
                # break
    # else:
    #     print ('Найдено 5 записей ',i)

    return links

# def get_page(html):
#
#
#     # print (session.post(url).text)
#     # print(url)
#     try:
#         soup = BeautifulSoup(html, 'lxml')
#     except:
#         print('Страница с торрентом не загружена')
#         exit(0)
#     try:
#         tds = soup.find('table', class_='w100p').find('a').get('href')
#     except:
#         print('Таблица со списком не обнаружена')
#         exit(0)
#     return tds

# Функция для скачивания торрент файла во временный с именем temp.torrent
def get_torrent_file (link, session):                                   # Скачать торрент файл
    file_torrent = session.get(link)
    if file_torrent.status_code == 200:
        with open('temp.torrent', 'wb') as f:  #
            f.write(file_torrent.content)  #
        f.close()
    else:
        return 1
    return 0


def autenticitate (): # Авторизация на сайте
    session = requests.session()
    url = 'http://kinozal.tv/takelogin.php'
    data = {'username':'expk13','password':'expk--'}
#    print (session.post(url, data=data).text)

def make_magnet_from_file(file) :                               # Создание magnet ссылок из torrent файла
    try:
        metadata = bencodepy.decode_from_file(file)
    except:
        # print('Вы использовали доступное Вам количество торрент-файлов в сутки')
        return 'Вы использовали доступное Вам количество торрент-файлов в сутки'
    subj = metadata[b'info']
    hashcontents = bencodepy.encode(subj)
    digest = hashlib.sha1(hashcontents).digest()
    b32hash = base64.b32encode(digest).decode()
    return 'magnet:?'\
             + 'xt=urn:btih:' + b32hash\
             + '&dn=' + metadata[b'info'][b'name'].decode()\
             + '&tr=' + metadata[b'announce'].decode()\
             # + '&xl=' + str(metadata[b'info'])

def main():

    # Для перебора страниц
    url = 'http://kinozal.tv/browse.php?s=lost' # Ссылка с поиском
    #url = 'http://kinozal.tv/browse.php'
    all_link = get_all_links(get_html(url),5)
    # print (all_link)
    for i in all_link:
         print ('id:',i[0],'Описание:',i[1])




    # autenticitate() # Авторизация


if __name__ == '__main__':
    main()