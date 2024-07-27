#! /usr/bin/env python

from bs4 import BeautifulSoup as bs
import requests
from structlog import get_logger

logger = get_logger()

def dolar()->str:
    headers:str = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15'
    url    :str = 'https://finance.yahoo.com/quote/TRY=X/'
    r           = requests.get(url)
    soup        = bs(r.text, 'html.parser')
    _div        = soup.find("div", {"class": "container yf-mgkamr"})
    try:
        _spans  = _div.find_all("span")
    except AttributeError as error:
        logger.error(error)
        return r.text
    _span       = _spans[0]
    dolar  :str = _span.text
    return dolar
result:str = dolar()
logger.debug(result)
