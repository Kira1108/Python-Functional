import requests
from lxml import etree
import logging
import os
logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))


def get_selector(url, **kwargs):

    try:
        html = requests.get(url, **kwargs)
        html.encoding = 'utf-8'
        html = html.text
    except:
        print('Unable to parse starturl')
        return None

    return etree.HTML(html)


def to_request(url, callback, **kwargs):
    logging.info('Scraping url: {}'.format(url))
    selector = get_selector(url, **kwargs)
    callback(selector)


def get_value(selector, xpath_str):
    result = selector.xpath(xpath_str)
    return '' if not result or len(result) == 0 else result[0]


def cvt_kv(list_os_string, sep = "："):
    tmp = {}
    for ele in list_os_string:
        if not sep in ele:
            continue
        k, v = ele.split(sep)
        tmp[k] = v

    return tmp
