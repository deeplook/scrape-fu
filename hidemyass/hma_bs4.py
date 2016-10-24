#!/usr/bin/env python

"""
Scrape first page of IP/port info from proxylist.hidemyass.com.

The scraping is done using Requests and BeautifulSoup, while
the information found is stored in a SQLite database (actually
two, one using SQLite3, and the other using SQLAlchemy).

Run with:

  python hma_bs4.py
"""

import re

import requests
from bs4 import BeautifulSoup

from unclutter import remove_clutter
import persist


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
        port = int(port)
        print('%2s %-15s %5d' % (i, ip, port))
        persist.store_sqlite3(ip, port)
        persist.store_sqlalchemy(ip, port)
