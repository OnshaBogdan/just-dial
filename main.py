import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException

import mongo

chrome_driver_path = '/usr/bin/chromedriver'
start_url = 'https://www.justdial.com/Delhi/Tutorials/nct-10502492/page-1'


def parse_list( url: str):
    print('parsing ', url)
    driver = create_chrome_driver()
    try:
        driver.get(url)
    except TimeoutException:
        driver.close()
        parse_list(url)
    time.sleep(3)

    element_urls = driver.find_elements_by_css_selector('#tab-5 > ul > li.cntanr')

    for element in element_urls:
        url = element.get_attribute('data-href')

        phone_elements = element.find_elements_by_css_selector('p.contact-info > span > a span')
        class_names = [element.get_attribute('class') for element in phone_elements]

        phone = decode_phone(class_names)
        title, address = parse_element(url)

        mongo.insert(dict(title=title, address=address, phone=phone))

    next_page_url = driver.find_element_by_css_selector('#srchpagination a[rel=next]').get_attribute('href')
    driver.close()

    parse_list(next_page_url)


def parse_element(url):
    driver = create_chrome_driver()
    try:
        driver.get(url)
    except TimeoutException:
        return parse_element(url)
    time.sleep(1.5)

    title = driver.find_element_by_css_selector('div.company-details span.fn').text
    address = driver.find_element_by_css_selector('#fulladdress span.lng_add').text

    driver.close()
    return title, address


def decode_phone(class_names: list):
    encoding = {
        'mobilesv icon-acb': '0',
        'mobilesv icon-yz': '1',
        'mobilesv icon-wx': '2',
        'mobilesv icon-vu': '3',
        'mobilesv icon-ts': '4',
        'mobilesv icon-rq': '5',
        'mobilesv icon-po': '6',
        'mobilesv icon-nm': '7',
        'mobilesv icon-lk': '8',
        'mobilesv icon-ji': '9',
        'mobilesv icon-fe': '(',
        'mobilesv icon-hg': ')',
        'mobilesv icon-ba': '-',
        'mobilesv icon-dc': '+',
    }

    phone = ''.join([encoding[class_name] for class_name in class_names])
    return phone


def create_chrome_driver() -> webdriver.Chrome:
    driver = webdriver.Chrome(chrome_driver_path)
    driver.set_page_load_timeout(60)
    driver.set_window_size(1024, 768)
    return driver


parse_list(start_url)
mongo.dump_json()
