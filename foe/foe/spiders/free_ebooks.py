#!/usr/bin/env python

"""
The PDFs seems to be downloaded sequentially (using requests)... :-(
Is there a trick grabbing them asynchronuously? If not, aiohttp should
do it...
"""

import re
import os

import scrapy
import requests


class FreeOreillyEbooksSpider(scrapy.Spider):
    name = 'freeebooksspider'
    cat = 'data'
    start_urls = ['http://shop.oreilly.com/category/ebooks/%s.do?sortby=publicationDate&page=1' % cat]

    def __init__(self, *args, **kwargs):
        scrapy.Spider.__init__(self, *args, **kwargs)

        # create output folder 
        os.makedirs(self.cat, exist_ok=True)

    def parse(self, response):
        paths = response.xpath('//span[@class="price"][contains(., "$0.00")]/../../../../div[@class="thumbheader"]/a/@href').extract()
        for path in paths:
            url = 'http://shop.oreilly.com' + path
            yield scrapy.Request(url, callback=self.parse_detail_page)

        # follow pagination links
        page_num = int(re.search('page=(\d+)', response.url).groups()[0])
        next_url = response.url.replace('page=%d' % page_num, 'page=%d' % (page_num + 1))
        yield scrapy.Request(next_url, callback=self.parse)

    def parse_detail_page(self, response):
        url_csp = response.url
        pdf_name = url_csp.split('/')[-1][:-4] + '.pdf'
        path = os.path.join(self.cat, pdf_name)
        if os.path.exists(path):
            pass
        else:
            u = 'http://www.oreilly.com/%s/free/files/%s' % (self.cat, pdf_name)
            print(u)
            pdf = requests.get(u).content
            open(path, 'wb').write(pdf)
            print('saved %s' % path)
