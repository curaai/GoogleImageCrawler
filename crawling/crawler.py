from crawling import filecontrol, parser
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

import requests
import re

#main class and use for dynamic web page
class Crawler:
    def __init__(self, keyword, limit):
        self.search_keyword = keyword
        self.keyword = self.checkDirectoryName(keyword)
        self.limit = limit
        self.error_occurred = 0
        self.controller = filecontrol.Controller()
        self.path = self.keyword + '/'
        self.default_format = '.jpg'

    #브라우저 생성 및 이미지 검색 페이지 return
    def init_browser(self):
        self.browser = webdriver.Chrome('.\WebDriver\chromedriver.exe')
        self.browser.get('https://www.google.com/imghp')

        search_field = self.browser.find_element_by_name('q')
        search_field.send_keys(self.search_keyword)
        search_field.send_keys(Keys.RETURN)

    #이미지가 없을 경우 스크롤해서 이미지를 추가함
    def scroll_down(self):
        scroll = self.browser.find_element_by_tag_name('html')
        scroll.send_keys(Keys.END)


    #url으로 파일 포맷을 지정하여 저장함
    def downloadimage(self, name, url):
        if not url:
            return -1

        if url.startswith('data'):
            self.controller.save_data_url(url)
            return 0

        file_format = url[-4:]
        if not file_format.startswith('.') or self.has_number(file_format):
            if file_format == 'jpeg':
                pass
            else:
                file_format = self.default_format

        file_name = self.path + name + file_format
        data = requests.get(url)
        #file_name에다가 저장
        try:
            res = self.controller.save_image(file_name, data)
        except OSError as e:
            res = -1

        return file_name

    def has_number(self, string):
        return bool(re.search(r'\d', string))

    def checkDirectoryName(self, str):
        string = ""

        for ch in str:
            if bool(re.search(r'\W', ch)):
                string += "_"
            else:
                string += ch

        return string