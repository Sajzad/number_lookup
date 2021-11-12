import os
import datetime
# import requests
import json
# import multiprocessing.forking
import sys
# import threading
import multiprocessing
from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from time import sleep
from bs4 import BeautifulSoup



number = "18436765277"

url = "https://api.telnyx.com/anonymous/v2/number_lookup/{}".format(number)
chrome_options = webdriver.ChromeOptions()
prefs = {
    'profile.managed_default_content_settings.images': 2,
}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-notifications')
chrome_options.add_argument('--disable-popup-blocking')
chrome_options.add_argument('--disable-logging')
chrome_options.add_argument('--log-level=3')
prefs={'disk-cache-size': 4096}
chrome_options.add_experimental_option('prefs', prefs)
chrome_options.add_argument('--proxy-server= {}'.format(proxy))
# chrome_options.add_argument('--proxy-server= socks4://184.185.2.146:47659')
chrome_options.add_argument('--headless')
driver = webdriver.Chrome(options=chrome_options)
driver.get(url)