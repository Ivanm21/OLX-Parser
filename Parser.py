#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests as rq
from bs4 import BeautifulSoup
import dateparser
import ast
from model import Add



def get_add_link(startingaddress):
    page = rq.get(startingaddress)
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding='utf-8')
    adds_table = soup.findAll("td", {"class": "offer"})

    for a in adds_table:
        addlink = a.find("a", {"class": "marginright5 link linkWithHash detailsLink"})
        if addlink is not None:
            yield addlink['href']


def get_next_page(address):
    # yeild address if it is first page
    if '?page=' not in address:
        yield address

    page = rq.get(address)
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding='utf-8')
    nextpage = soup.find('span', {"class": "fbold next abs large"})
    if nextpage is not None:
        child = nextpage.find('a')['href']
        if child is not None:
            yield child
            for x in get_next_page(child):
                yield x


def parse_add(addlink):
    addObject = Add.Add(addlink)
    page = rq.get(addlink)
    soup = BeautifulSoup(page.content, 'html.parser', from_encoding='utf-8')

    # Check if add is promoted
    addObject.promoted = is_promoted(addlink)

    # Check if Add was [ublished from mobile phone
    addObject.published_from_mobile = is_published_from_mobile(soup)

    # Get Price Dictionary with Price, Currency, Negotiable
    priceDic = get_price(soup)
    addObject.price = priceDic['price']
    addObject.currency = priceDic['currency']
    addObject.negotiable = priceDic['negotiable']

    # Get add Text, Title, District
    addObject.text = get_add_text(soup)
    addObject.add_title = get_add_title(soup)
    addObject.district = get_add_district(soup)

    #Get Phone number
    addObject.phone_number = get_phone_number(addlink)

    # Parsing fields available in details table: type of add, quantity of rooms, type of rent, type of building
    addObject.addType = get_add_type(soup)
    addObject.rooms = get_rooms(soup)
    addObject.building_type = get_building_type(soup)

    # Adding date and number of the add
    addObject.date = get_add_date(soup)
    addObject.number = get_add_number(soup)

    # Adding links to images
    addObject.image_links = get_photo_links(soup)

    return addObject


def get_phone_number(address):
    iD = address[address.find('ID') + 2:address.find('.html')]
    headers = {'Referer': address}

    s = rq.Session()
    page = s.get(address)

    soup = BeautifulSoup(page.content, 'html.parser',from_encoding='utf-8')

    try:
        phoneToken = soup.find('section', {'id': 'body-container', 'class': 'offer-section'}).findChild(
            'script').text.strip()
        phoneToken = phoneToken[phoneToken.find('var phoneToken = \'') + len('var phoneToken = \''):phoneToken.find('\';')]
    except AttributeError:
        return 0

    try:
        phoneResponse = s.get('https://www.olx.ua/ajax/misc/contact/phone/' + iD + '/?pt=' + phoneToken, headers=headers)
        phoneResponse.raise_for_status()
        phone_number = ast.literal_eval(phoneResponse.content.decode('UTF-8'))
        return phone_number['value']

    except rq.exceptions.HTTPError:
        return 0


def is_promoted(link):
    promoted = False

    if 'promoted' in link:
        promoted = True

    return promoted


def get_price(soup):
    price_dict = {'price':0 ,'currency':'uah','negotiable': False, }

    price_element = soup.find('div', {'class': 'price-label'})
    if price_element is not None:
        if price_element.find('small') is not None:
            price_element = price_element.text.replace('Договорная', '')
            price_dict['negotiable'] = True

        if 'грн' in price_element.text:
            price_element = price_element.text.replace('грн.', '')
            price_dict['currency'] = 'uah'

        if '$' in price_element.text:
            price_element = price_element.text.replace('$', '')
            price_dict['currency'] = 'usd'

        if '€' in price_element.text:
            price_element = price_element.text.replace('€', '')
            price_dict['currency'] = 'eur'

        price_dict['price'] = price_element.text.replace(' ', '').strip()

    return price_dict


def get_add_text(soup):
    try:
        text = soup.find('div', {'class': 'clr', 'id': 'textContent'}).text.strip()
        return text
    except AttributeError:
        text = ''
        return text


def get_add_title(soup):
    try:
        add_title = soup.find('div', {'class': 'offer-titlebox'}).findChild('h1').text.strip()
        return add_title
    except AttributeError:
        add_title = '-'
        return add_title


def get_add_district(soup):
    try:
        district = soup.find('div', {'class': 'offer-titlebox__details'})\
            .findChild('a').text.strip()
        return district
    except AttributeError:
        district = ''
    return district


def get_add_type(soup):
    addType = ''
    try:
        detailstable = soup.find('table', {'class': 'details fixed marginbott20 margintop5 full'})
        advertizerTable = detailstable.find('th', text='Объявление от').parent
        addType = advertizerTable.find('td').text.strip()
    except AttributeError:
        return addType

    return addType


def get_rooms(soup):
    rooms = 0
    try:
        detailstable = soup.find('table', {'class': 'details fixed marginbott20 margintop5 full'})
        roomstable = detailstable.find('th', text='Количество комнат').parent
        rooms = roomstable.find('td').text.strip()
    except AttributeError:
        return rooms

    return rooms


def get_rent_type(soup):
    rent_type = ''
    try:
        detailstable = soup.find('table', {'class': 'details fixed marginbott20 margintop5 full'})
        rent_type_table = detailstable.find('th', text='Тип аренды').parent
        rent_type = rent_type_table.find('td').text.strip()
    except AttributeError:
        return rent_type

    return rent_type

def get_building_type(soup):
    building_type = ''
    try:
        detailstable = soup.find('table', {'class': 'details fixed marginbott20 margintop5 full'})
        building_type_table = detailstable.find('th', text='Тип').parent
        building_type = building_type_table.find('td').text.strip()
    except AttributeError:
        return building_type

    return building_type


def get_add_date(soup):
    # Adding Date when add was created and number of the add.
    date = ''
    try:
        date_and_number = soup.find('div', {'class': 'offer-titlebox__details'}).findChild('em')
        date_and_number = date_and_number.text.strip().replace(' ', '')
        if '\nв' in date_and_number:
            date = dateparser.parse(date_and_number[date_and_number.find('\nв') + 3:date_and_number.find(',Номер')])
        elif ':в' in date_and_number:
            date = dateparser.parse(date_and_number[date_and_number.find(':в') + 3:date_and_number.find(',Номер')])
    except AttributeError:
        return date

    return date


def is_published_from_mobile(soup):
    published_from_mobile = False
    mobileicon = soup.find('i', {'data-icon': 'mobile'})
    mobileappslink = soup.find('a',{'href':'https://www.olx.ua/mobileapps/'})
    if (mobileicon  is not None) & (mobileappslink is not None):
        published_from_mobile = True

    return published_from_mobile


def get_add_number(soup):
    # Adding Date when add was created and number of the add.
    number = ''
    try:
        date_and_number = soup.find('div', {'class': 'offer-titlebox__details'}).findChild('em').text.strip().replace(' ', '')
        number = date_and_number[date_and_number.find('объявления:') + len('объявления:'):]
    except AttributeError:
        return number
    return number


def get_photo_links(soup):
    image_links = []
    images = soup.findAll('div', {'class': 'tcenter img-item'})
    for i in images:
        link = i.find('img')
        image_links.append(link['src'])

    return image_links
