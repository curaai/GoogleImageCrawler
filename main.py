from crawling import crawler
from urllib.request import urlopen
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawling.parser import Parser

import time


def main():
    # print('구글에서 다운받고 싶은 이미지를 입력해주세요')
    # keyword = input("입력 : ")
    # count = int(input("이미지의 개수 : "))

    downloader = crawler.Crawler('트와이스', 10)
    parser = Parser()

    print('Chrome 브라우저가 열릴 수 있습니다.')
    downloader.init_browser()
    downloader.controller.makedirectory(downloader.keyword)
    
    i = 0
    download_count = 0
    
    while True:
        if download_count >= downloader.limit:
            break

        result_link = parser.result_image_page(downloader.browser.page_source, i)
        if result_link == -1:
            downloader.scroll_down()
            result_link = parser.result_image_page(downloader.browser.page_source, i)

        downloader.browser.get("https://google.com" + result_link)

        image_url = parser.get_image_url(downloader.browser.page_source, 'irc_mi')
        res = downloader.downloadimage(str(download_count), image_url)

        if res == -1:
            image_url = parser.get_image_url(downloader.browser.page_source, 'irc_mut')
            downloader.downloadimage(str(download_count), image_url)

        download_count += 1
        print(str(round(download_count / downloader.limit, 2) * 100) + "% downloaded")

        i += 1
        downloader.browser.back()

    print('download successed')

main()