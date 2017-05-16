from bs4 import BeautifulSoup
from urllib.request import *
from urllib.error import HTTPError
import os
import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class Crawler():
    def __init__(self, keyword, limit):
        self.keyword = keyword
        self.limit = limit
        self.error_occurred = 0

    def crawling(self):
        browser = webdriver.Chrome(".\WebDriver\chromedriver.exe")
        browser.get("https://www.google.com/imghp")

        search_field = browser.find_element_by_name("q")
        search_field.send_keys(self.keyword)
        search_field.send_keys(Keys.RETURN)

        i = 0
        download_count = 0

        while True:
            if download_count >= self.limit:
                break
            search_page = self.getsearchpage(browser.page_source, i)
            browser.get("https://google.com" + search_page)
            time.sleep(1.5)

            image_url = self.getimageurl(browser.page_source)

            res = self.downloadimage(str(download_count), image_url)
            if res == 0:
                download_count += 1
                #progress status
                print(str(round(download_count / self.limit, 2) * 100) + "% downloaded")

            i += 1
            browser.back()
            time.sleep(1.5)

        browser.quit()

    #이미지 검색결과 창(url)을 반환
    def getsearchpage(self, html_source, count):
        bs = BeautifulSoup(html_source, 'html.parser')
        return bs.find("div", {"data-ri": str(count)}).find('a')['href']

    #웹코드로부터 img가 있을만한 link를 찾아 반환
    def getimageurl(self, html_source):
        bs = BeautifulSoup(html_source, 'html.parser')

        #return image_url in html code
        for line in bs.findAll('img', {"class": "irc_mi"}):
            if len(line['class']) == 1:
                return line['src']

        return None

    #if success to download return 0 else return -1
    def downloadimage(self, name, url):
        file_format = url[-4:]
        if not '.' in file_format:
            file_format = '.jpg'

        flag = 0

        f = open(name + file_format, "wb")
        try:
            data = urlopen(url).read()
            #잘못된 이미지일 경우 크기가 2kb보다 작음 -> 제거
            if len(data) < 2000:
                os.remove(name + file_format)
                return -1

            f.write(data)

        except Exception as e:
            flag = -1
        finally:
            f.close()

        return flag