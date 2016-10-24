"""
Some help for uncluttering HTML text.
"""

import re

from bs4 import BeautifulSoup


def remove_clutter(markup_text, rm_whitespace=True):
    """
    Remove div/span clutter intended to make scraping HTML text harder.
    """
    soup = BeautifulSoup(markup_text, 'lxml')

    # remove elements specified inline to be not displayed
    for el in soup.findAll(style='display:none'):
        el.replaceWith('')

    # remove elements specified by a class to be not displayed
    style = soup.find('style')
    if style:
        hidden = re.findall('\.([\w\-]+){display:none}', style.text.replace('\n', ''), re.S)
        for h in hidden:
            for el in soup.findAll(class_=h):
                el.replaceWith('')

        # remove style element defining classes to be not displayed
        soup.find('style').replaceWith('')

    try:
        result = soup.span.text
    except AttributeError:
        result = soup.text
    
    # remove whitespace
    if rm_whitespace:
        result = result.replace('\n', '').strip()

    return result
