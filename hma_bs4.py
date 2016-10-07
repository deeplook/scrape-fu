#!/usr/bin/env python

import re

import requests
from bs4 import BeautifulSoup

from unclutter import remove_clutter


def read_table():
    """
    Read a table from a page on the web, that tries making it a little harder.
    """
    url = 'http://proxylist.hidemyass.com/'
    html = requests.get(url).text
    soup = BeautifulSoup(html, 'lxml')
    table = soup.find(class_='hma-table')
    result = []
    for j, tr in enumerate(table.findAll('tr')[1:]):
        for i, td in enumerate(tr.findAll('td')):
            if i == 1:
                ip = remove_clutter(str(td.find('span')))
            elif i == 2:
                port = td.text.strip()
            else:
                continue
        result.append((ip, port))
    return result


if __name__ == '__main__':
    tab = read_table()
    for i, (ip, port) in enumerate(tab):
        print('%2s %-15s %5s' % (i, ip, port))
