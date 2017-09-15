#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests as rq
import bs4
from bs4 import BeautifulSoup

page = rq.get('https://www.olx.ua/nedvizhimost/arenda-kvartir/dolgosrochnaya-arenda-kvartir/kiev/')


def getaddlinks(page):
    soup = BeautifulSoup(page.content, 'html.parser')

    ListOfHrefs = []
    for a in soup.findAll("a", {"class": "marginright5 link linkWithHash detailsLink"}):
        ListOfHrefs.append(a['href'])

    return ListOfHrefs


list = getaddlinks(page)


