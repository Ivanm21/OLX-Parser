#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests as rq
from bs4 import BeautifulSoup
import re
import dateparser

address = 'https://www.olx.ua/nedvizhimost/arenda-kvartir/dolgosrochnaya-arenda-kvartir/kiev/'


def get_add_link(startingaddress):
    page = rq.get(startingaddress)
    soup = BeautifulSoup(page.content, 'html.parser',from_encoding='utf-8')
    adds_table = soup.find("table",{"id": "offers_table"})

    for a in adds_table.findAll("tr", {"class": "wrap"}):
        addlink = a.find("a",{"class": "marginright5 link linkWithHash detailsLink"})
        if addlink is not None:
            yield addlink['href']


def get_next_page(address):
    page = rq.get(address)
    soup = BeautifulSoup(page.content, 'html.parser',from_encoding='utf-8')
    nextpage = soup.find('span',{"class":"fbold next abs large"})
    if nextpage is not None:
        child = nextpage.find('a')['href']
        if child is not None:
            yield child
            for x in get_next_page(child):
                yield x


def parse_add(addlink):
    page = rq.get(addlink)
    soup = BeautifulSoup(page.content, 'html.parser',from_encoding='utf-8')

    price = soup.find('div',{'class':'price-label'}).text.encode('utf-8').replace(" ",'').replace('грн.','')
    text = soup.find('div',{'class': 'clr','id':'textContent'}).text.encode('utf-8').strip()

    detailstable = soup.find('table',{'class':'details fixed marginbott20 margintop5 full'})


    if detailstable.find('th', text='Объявление от') is not None:
        advertizerTable = detailstable.find('th', text='Объявление от').parent
        addType = advertizerTable.find('td').text.encode('utf-8').strip()


    if detailstable.find('th',text= 'Количество комнат') is not None:
        roomstable = detailstable.find('th', text='Количество комнат').parent
        rooms = roomstable.find('td').text.encode('utf-8').strip()


    if detailstable.find('th', text='Тип аренды') is not None:
        rent_type_table = detailstable.find('th', text='Тип аренды').parent
        rent_type = rent_type_table.find('td').text.encode('utf-8').strip()


    if detailstable.find('th',text='Тип') is not None:
        building_type_table = detailstable.find('th', text='Тип').parent
        building_type = building_type_table.find('td').text.encode('utf-8').strip()


    add_title = soup.find('div',{'class':'offer-titlebox'}).findChild('h1').text.encode('utf-8').strip()

    district = soup.find('div',{'class':'offer-titlebox__details'}).findChild('a').text.encode('utf-8').strip()

    date_and_number = soup.find('div',{'class':'offer-titlebox__details'}).findChild('em').text.encode('utf-8').strip().replace(' ','')

    date = dateparser.parse(date_and_number[date_and_number.find(':в')+3:date_and_number.find(',Номер')])
    number = date_and_number[date_and_number.find('объявления:')+ len('объявления:'):]

    image_links = []
    images = soup.findAll('div',{'class':'tcenter img-item'})
    for i in images:
        link = i.find('img')
        image_links.append(link['src'])



    print (image_links)


# parse_add('https://www.olx.ua/obyavlenie/1-komnatnaya-metro-10-minut-peshim-shagom-IDuX0sg.html#39f9431a35;promoted')




pages = get_next_page(address)
# for p in pages:
#     print (p)
# links = get_add_link(pages.next())
# for p in pages:
#     print(p)

# for p in pages:
#     links = get_add_link(p)
#     for l in links:
#         print l



# def getaddlinks(page):
#     soup = BeautifulSoup(page.content, 'html.parser')
#     offers = soup.find("table",{"id":"offers_table"})
#
#     ListOfHrefs = [[1,1]]
#     for a in offers.findAll("tr", {"class": "wrap"}):
#         link = a.find("a",{"class":"marginright5 link linkWithHash detailsLink"})
#         date = a.find("p",{"class":"color-9 lheight16 marginbott5 x-normal"})
#         tup = (link['href'],date.text.encode('utf-8'))
#         ListOfHrefs.append(tup)
#
#     return ListOfHrefs
#
# def getNextPage(page):
#     soup = BeautifulSoup(page.content,'html.parser')
#     nextpage = soup.find('span',{"class":"fbold next abs large"})
#     child = nextpage.find('a')['href']
#     return child
#
# def writeToCSV(page,file):
#     with open( file, "wb") as csv_file:
#         writer = csv.writer(csv_file, delimiter=',')
#         for line in page:
#             writer.writerow(line)
#
#
# list = getaddlinks(page)
# writeToCSV(list,"/Users/Ivanm/Desktop/test.csv")




# headers = {'Referer':'https://www.olx.ua/obyavlenie/1-komnatnaya-metro-10-minut-peshim-shagom-IDuX0sg.html'}
#
# s = rq.Session()
# s.headers.update({'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'})
#
# page = s.get('https://www.olx.ua/ajax/misc/contact/phone/uX0sg/?pt=3df800a1c84ac125690512a3d9e69fd0f5ab2db63e64beeab7ba5dabf95fc9a26c8d83c9b0062ed979b033ff142bee179b7db9800ccda3b488d87cd7b9062fe6',headers=headers)
#
# phoneToken = '071bac232eff09666fdf4eeb268485df9a6d174dcca3a6eae6b52c9119e1751a9f899b94e21a242ae8147a36b3dd442ddac4e55334b51cff12aa49b021cdd7fc'
#
# print(page.content)
# print (page.headers)
# print (page.cookies)
# print (page.raw)

