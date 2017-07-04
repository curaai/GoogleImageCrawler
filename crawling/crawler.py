from crawling import filecontrol, parser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import requests
import re
import time


#main class and use for dynamic web page
class Crawler:
    def __init__(self, keyword, limit):
        self.search_keyword = keyword
        self.limit = limit
        self.error_occurred = 0
        self.default_format = '.jpg'

    #브라우저 생성 및 이미지 검색 페이지 return
    def init_browser(self):
        self.browser = webdriver.Chrome('.\WebDriver\chromedriver.exe')
        self.browser.get('https://www.google.com/imghp')

        search_field = self.browser.find_element_by_name('q')
        search_field.send_keys(self.search_keyword)
        search_field.send_keys(Keys.RETURN)

    #원하는 이미지의 사이즈를 설정함
    def set_size(self, width, height):
        self.browser.find_element_by_class_name("hdtb-tl").click()
        self.browser.find_element_by_class_name("hdtb-mn-hd").click()
        self.browser.find_element_by_class_name("exylnk").click()

        widthField = self.browser.find_element_by_xpath('//*[@class="ktf mini exymm exyw"]')
        heightField = self.browser.find_element_by_xpath('//*[@class="ktf mini exymm exyh"]')

        widthField.send_keys(width)
        heightField.send_keys(height)
        widthField.send_keys(Keys.RETURN)

    #이미지가 없을 경우 스크롤해서 이미지를 추가함
    def scroll_down(self):
        self.browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)

    def click_image(self, count):
        try:
            self.browser.find_element_by_xpath("//div[@data-ri = '{}']".format(str(count))).click()
        except Exception:
            return -1
