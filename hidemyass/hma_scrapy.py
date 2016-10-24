#!/usr/bin/env python

"""
Scrape first page of IP/port info from proxylist.hidemyass.com.

The scraping is done using Scrapy, while the information found
is stored in a SQLite database (actually two, one using SQLite3,
and the other using SQLAlchemy).

Run with:

  scrapy runspider -o out.json --nolog hma_scrapy.py
"""

import scrapy

from unclutter import remove_clutter
import persist


class HideMyAssSpider(scrapy.Spider):
    name = 'hmaspider'
    start_urls = ['http://proxylist.hidemyass.com/']

    def parse(self, response):
        # get ports column (easy)
        xpath = '//*[@id="listable"]/tbody/tr/td[3]/text()'
        rows3 = response.selector.xpath(xpath)
        ports = [int(r.extract().strip()) for r in rows3]

        # get IP column (harder, because it's cluttered)
        xpath = '//*[@id="listable"]/tbody/tr/td[2]/span'
        rows2 = response.selector.xpath(xpath)
        ips = [remove_clutter(r.extract()) for r in rows2]

        for ip, port in zip(ips, ports):
            # store in SQLite databases
            persist.store_sqlite3(ip, port)
            persist.store_sqlalchemy(ip, port)

            # write into log file
            yield {'ip': ip, 'port': port}
