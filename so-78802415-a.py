#! /usr/bin/env python

#import nest_asyncio
#nest_asyncio.apply()

#from itertools import repeat
from itertools import cycle
from random import shuffle
import time
import threading
import asyncio
from typing import AsyncIterator, Callable, List, Dict, Any, Union, Optional, ParamSpec, TypeVar, TypeAlias
from traceback import format_exception
from traceback import TracebackException
from traceback import format_exc
from typing import Iterable, Tuple
#from threading import Event as ThreadEvent
from typing import Iterator
from typing import ParamSpec, TypeVar
from uvicorn import run as urun
from os import environ
#from threading import Condition
from asyncio     import AbstractEventLoop
from typing      import Coroutine
from typing import Sequence
from typing import Sequence, Optional
#from threading import Thread
from asyncio import get_running_loop
from typing import Union, Optional
from os import getenv
from typing import Union
from datetime import datetime
from collections.abc import Coroutine
from typing import Union
import re
import asyncio
import os
from typing import Any
from typing import Callable
from typing import Dict
from typing import Iterable
from typing import List
from typing import Literal
from typing import Iterator
from typing import Optional
#from typing import TypeAlias
from typing import Union
#from tempfile import NamedTemporaryFile
from shutil import which
from pathlib import Path

from structlog import get_logger

#from asynctempfile             import NamedTemporaryFile
import aiofiles
from aiofiles.tempfile             import NamedTemporaryFile
from bs4 import BeautifulSoup
from fastapi import Response, status
from fastapi.responses import FileResponse
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
#import hypothesis
#from hypothesis import strategies as st
import numpy as np

import selenium_async
from selenium_async import Firefox
from selenium_async import FirefoxOptions
from selenium_async import Options
from selenium_async import Pool
from selenium_async import WebDriver
from selenium import webdriver
from selenium.common.exceptions import SessionNotCreatedException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
from selenium.webdriver import Chrome
from selenium.webdriver import ChromeOptions
from selenium.webdriver import EdgeOptions
from selenium.webdriver import Edge
from selenium.webdriver import Ie
from selenium.webdriver import IeOptions
#from selenium.webdriver import OperaOptions
from selenium.webdriver import Remote
#from selenium.webdriver.chrome import service
#from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary # fuck
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.ie.service import Service as IEService
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.core.os_manager import ChromeType
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.microsoft import IEDriverManager
from webdriver_manager.opera import OperaDriverManager

logger      = get_logger()
#P:ParamSpec = ParamSpec('P')
#T:TypeVar   = TypeVar  ('T')

##
#
##


def get_firefox_options(
        decorated:bool=True,
        fatass   :bool=False,
        headless :bool=False,
        sandbox  :bool=True,
)->FirefoxOptions:
    options     :FirefoxOptions = FirefoxOptions()         # normal Options() from selenium
    options.browser             = "firefox"                # tryna make selenium_async cooperate when the browser needs to be restarted
    if (not decorated):                                    # window "decorations" ?
        options.add_argument('disable-infobars')
    if headless:                                           # show the browser ?
        options.add_argument("--headless")                 # https://stackoverflow.com/questions/46920243/how-to-configure-chromedriver-to-initiate-chrome-browser-in-headless-mode-throug/49582462#49582462
        options.add_argument("-headless")                  # chromium
    options.headless            = headless
    if sandbox:                                            # step on your toes ?
        options.add_argument("--disable-extensions")
        options.add_argument("--sandbox")
        options.add_argument("-safe-mode")
        #options.add_argument("-ProfileManager")
        #options.add_argument("-P Default_User")
        #options.add_argument("-P ")
    #else:
    #    options.add_argument("-P default-esr")
    #    options.add_argument("-new-window")
    if (not fatass):                                       # be a fat PoS ?
        pass
    options.add_argument('start-maximized')
    return options
def get_chrome_options(
        decorated:bool=False,
        fatass   :bool=False,
        headless :bool=False,
        sandbox  :bool=False,
)->ChromeOptions:  
    options:ChromeOptions       = ChromeOptions()
    options.browser             = "brave-browser-stable" # TODO
    if (not decorated):
        options.add_argument("--hide-scrollbars")
    if headless:
        options.add_argument("--headless")
        options.add_argument("-headless")
    options.headless            = headless
    if sandbox:
        options.add_argument("--disable-extensions")
        options.add_argument("--sandbox")
    else:
        logger.debug('no sandbox')
        options.add_argument('--user-data-dir=./somewhere')
        options.add_argument('--profile-directory=somewhere')
    assert (not sandbox)
    if (not fatass):
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--single-process")
        options.add_argument("--disable-gpu")
    options.add_argument("--ignore-certficate-errors")
    return options
def get_ie_options(
        decorated:bool=False,
        fatass   :bool=False,
        headless :bool=True,
        sandbox  :bool=True,
)->IeOptions:
    options:IeOptions           = IeOptions()
    options.browser             = "iexplore" # TODO 
    return options
def get_edge_options(
        decorated:bool=False,
        fatass   :bool=False,
        headless :bool=True,
        sandbox  :bool=True,
)->EdgeOptions:
    options:EdgeOptions         = EdgeOptions()
    options.browser             = "edge"     # TODO
    return options
def get_opera_options(
        decorated:bool=False,
        fatass   :bool=False,
        headless :bool=True,
        sandbox  :bool=True,
)->EdgeOptions:
    options:Options             = Options()
    options.browser             = "opera"    # TODO
    return options

def get_firefox_service()->FirefoxService:                 # download and install fat PoS #1
    try:
        executable_path   = GeckoDriverManager().install()
    except AttributeError as error:
        logger.exception(error)
        #executable_path  = which('firefox')
        executable_path   = which('geckodriver') # TODO
    return FirefoxService(executable_path)

def get_chrome_service()->ChromeService:                   # https://stackoverflow.com/questions/69774045/selenium-chromedriver-issue-using-webdriver-manager-for-python
    try:
        executable_path   = ChromeDriverManager().install()
    except AttributeError as error:
        logger.exception(error)
        #executable_path  = which('chrome')
        executable_path   = which('chromedriver') # TODO
    return ChromeService(executable_path)

def get_chromium_service()->ChromeService:
    try:
        executable_path   = ChromeDriverManager(chrome_type=ChromeType.CHROMIUM).install()
    except AttributeError as error:
        logger.exception(error)
        executable_path   = which('chromium') # TODO
    return ChromeService(executable_path)

def get_brave_service()->ChromeService:
    try:
        executable_path   = ChromeDriverManager(chrome_type=ChromeType.BRAVE).install()
    except AttributeError as error:
        logger.exception(error)
        executable_path   = which('chromedriver')
    return ChromeService(executable_path)

def get_edge_service()->EdgeService:
    try:
        executable_path   = EdgeChromiumDriverManager().install()
    except AttributeError as error:
        logger.exception(error)
        executable_path   = which('edge-browser') # TODO
    return EdgeService(executable_path)

def get_ie_service()->IEService:
    try:
        executable_path   = IEDriverManager().install()
    except AttributeError as error:
        logger.exception(error)
        executable_path   = which('ie-browser') # TODO
    return IEService(executable_path)

def get_opera_service()->ChromeService:
    try:
        executable_path   = OperaDriverManager().install()
    except AttributeError as error:
        logger.exception(error)
        executable_path   = which('opera-browser') # TODO
    service:ChromeService = ChromeService(executable_path)
    service.start()
    return service

def get_firefox_driver(options:FirefoxOptions)->WebDriver: # selenium_async isn't too smart under the hood. I read all of it in order to do this.
    service:FirefoxService = get_firefox_service()         # download and install
    return Firefox(                                        # normal Firefox from selenium
        options=options,
        service=service,
    )                                                      # TODO how to detect when this fat shit gets killed
def get_chrome_driver(options:ChromeOptions, provider:str)->WebDriver:
    service:Optional[ChromeService] = None
    if (provider == "chrome"):
        service = get_chrome_service()
    if (provider == "chromium"):
        service = get_chromium_service()
    if (provider == "brave"):
        service = get_brave_service() 
    if (service is None):
        raise ValueError(provider)
    return Chrome(
            options=options,
            service=service,
    )
def get_edge_driver(options:EdgeOptions)->WebDriver:
    service:EdgeService = get_edge_service()
    return Edge(
            options=options,
            service=service,
    )
def get_ie_driver(options:IeOptions)->WebDriver:
    service:IEService = get_ie_service()
    return Ie(
            options=options,
            service=service,
    )
def get_opera_driver(options:ChromeOptions)->WebDriver:
    service:ChromeService = get_opera_service()
    return Remote(service.service_url, options=options)
   
def get_pool_helper(driver:WebDriver, options:Options)->Pool:
    driver.set_window_size(1600,800)
    pool   :Pool            = Pool(max_size=1)             # we've gotta prevent that stupid-ass library from trying to allocate any Firefox's without the service setting
    pool.resources[options] = [driver,]                    # populate its internal mapping and make sure it doesn't f with my settings
    return pool
def get_firefox_pool()->Tuple[Pool,FirefoxOptions]:
    options:FirefoxOptions  = get_firefox_options()
    driver :WebDriver       = get_firefox_driver(options)
    pool   :Pool            = get_pool_helper(driver, options)
    return (pool, options,)
def get_chrome_pool(provider:str)->Tuple[Pool,ChromeOptions]:
    options:ChromeOptions   = get_chrome_options(provider)
    if (provider == "brave"):
        options.browser         = "chromium"
        options.binary_location = which("brave-browser-stable")
    driver :WebDriver       = get_chrome_driver(options, provider)
    pool   :Pool            = get_pool_helper(driver, options)
    return (pool, options,)
def get_edge_pool()->Tuple[Pool,EdgeOptions]:
    options:EdgeOptions     = get_edge_options()
    driver :WebDriver       = get_edge_driver(options)
    pool   :Pool            = get_pool_helper(driver, options)
    return (pool, options,)
def get_ie_pool()->Tuple[Pool,IeOptions]:
    options:IeOptions       = get_ie_options()
    driver :WebDriver       = get_ie_driver(options)
    pool   :Pool            = get_pool_helper(driver, options)
    return (pool, options,)
def get_opera_pool()->Tuple[Pool,ChromeOptions]:
    options:ChromeOptions   = get_opera_options()
    driver :WebDriver       = get_opera_driver(options)
    pool   :Pool            = get_pool_helper(driver, options)
    return (pool, options,)
def get_pool(provider:str)->Tuple[Pool,Options]:
    if (provider == "firefox"):                        # crap #1        by Mozzerelli
        return get_firefox_pool()
    if (provider in ["chrome", "chromium", "brave",]): # craps #2, 3, 4 by Gaggle
        return get_chrome_pool(provider)
    if (provider == "ie"):                             # craps #5,6     by WinDoze
        return get_ie_pool()
    if (provider == "edge"):
        return get_edge_pool()
    if (provider == "opera"):                          # crap #7        by Crapple ?
        return get_opera_pool()
    raise ValueError(provider)

def random_wait(mean_arrival_rate:Optional[float])->None:
    """ naive randomized wait to simulate human reflexes """
    if (mean_arrival_rate is None):                             # Set the mean arrival rate for the Poisson distribution
        return
    logger.debug('random wait start')
    random_wait_time:int = np.random.poisson(mean_arrival_rate) # Generate a random wait time following a Poisson distribution
    assert isinstance(random_wait_time,int)
    time.sleep(random_wait_time)                                # Adjust this value based on your simulation requirements
    logger.debug('random wait done')

from selenium.webdriver.remote.webelement import WebElement

def get_app(provider:str)->Coroutine[Optional[str]]:
    app          :FastAPI             = FastAPI()
    pool         :Pool
    options      :Options
    pool, options                     = get_pool (provider)
    timeout      :int                 = 30

    def find_element(driver:WebDriver, mean_arrival_rate:Optional[float], *condition:Tuple[By,str], fallback:Optional[WebElement]=None)->WebElement:
        """
        attempt to click an element by some number of conditions
        if not found, then send the enter key to the fallback element
        raise an error if nothing happened
        """
        nonlocal timeout
        logger.debug('find_element')
        for by, cond in condition:
            logger.debug('searching %s %s', by, cond)
            try:
                element:WebElement = WebDriverWait(driver, timeout).until( EC.presence_of_element_located((by, cond)))
                #element.click()
                return element
            except NoSuchElementException as e:
                logger.error('could not find element: %s', e)
            except TimeoutException as e:
                logger.error('timed out looking for element: %s', e)
        if (fallback is None):
            raise NoSuchElementException()
        fallback.send_keys(Keys.RETURN)
        return fallback

    async def run()->Optional[str]:
        _url             :str             = 'https://finance.yahoo.com/quote/TRY=X/'
        limit            :int             = 1
        mean_arrival_rate:Optional[float] = None

        def helper(driver:WebDriver)->Optional[str]:
            """
            Parse it:

            <fin-streamer class="livePrice yf-mgkamr" data-symbol="TRY=X" data-testid="qsp-price" data-field="regularMarketPrice" data-trend="none" data-pricehint="4" data-value="32.9042" active=""><span>32.9042</span></fin-streamer>
            """

            logger.debug('grab url')
            driver.get(_url) # TODO params, headers, auth       
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")            # get the whole page
            logger.debug('loaded page %s', _url)

            _price = find_element(driver, None, # don't need to make it think we're not a bot, so no wait time
                (By.XPATH, "//fin-streamer[@data-symbol='TRY=X']"),
                (By.XPATH, "//fin-streamer[@data-testid='qsp-price']"),
                (By.XPATH, "//fin-streamer[@data-field='regularMarketPrice']"),
                fallback=None) # fallback is used to press 'enter' when clicking 'next' fails. don't worry about it
            return _price.get_attribute('data-value')
        try:
            async with selenium_async.use_browser(options=options, pool=pool) as driver:
                result:Optional[str] = await asyncio.to_thread(helper, driver)
                await logger.ainfo('result: %s', result)
        except AttributeError as error:
            #await logger.aerror(error)
            logger.error(error)
        return result

    return run

def main()->None:
    provider:str     =      getenv('PROVIDER',            'brave')
    app     :Coroutine[Optional[str]] = get_app(provider)
    asyncio.run(app())

if __name__ == '__main__':
    main()
