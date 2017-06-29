# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
from crawling.crawler import Crawler
from crawling.parser import Parser
from threading import Thread

from PyQt4 import QtCore, QtGui
import PyQt4.uic

from bs4 import BeautifulSoup


class MainDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)

        self.ui = PyQt4.uic.loadUi("GUI\design.ui", self)

        self.ui.dirSelect.clicked.connect(self.selectDir)
        self.ui.startCrawling.clicked.connect(lambda x: Thread(target=self.start_crawling()).start)

    def selectDir(self):
        self.dirPath = str(QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\',
                                                         QtGui.QFileDialog.ShowDirsOnly))

    def temp(self):
        Thread(target=self.start_crawling).start()

    def start_crawling(self):
        self.progressBar.setValue(0)

        self.keyword = self.keyword_edit.text().strip()
        widthScale = self.scale_width_edit.text()
        heightScale = self.scale_height_edit.text()
        self.limit = int(self.image_count_edit.text())

        downloader = Crawler(self.keyword, self.limit, self.dirPath)
        parser = Parser()

        # alert 창 띄우기
        downloader.init_browser()
        if widthScale != "" and heightScale != "":
            downloader.set_size(widthScale, heightScale)
        downloader.controller.makedirectory(downloader.keyword)

        i = 0
        downloadCount = 0
        gauge = 0

        while True:
            if downloadCount >= downloader.limit:
                break

            resultLink = parser.result_image_page(downloader.browser.page_source, i)
            if resultLink == -1:
                downloader.scroll_down()
                resultLink = parser.result_image_page(downloader.browser.page_source, i)

            downloader.browser.get("https://google.com" + resultLink)

            imageUrl = parser.get_image_url(downloader.browser.page_source, 'irc-mi')
            res = downloader.downloadimage(str(downloadCount + 1), imageUrl)

            if res == -1:
                imageUrl = parser.get_image_url(downloader.browser.page_source, 'irc_mut')
                res = downloader.downloadimage(str(downloadCount + 1), imageUrl)

            downloadCount += 1
            temp = round(downloadCount / downloader.limit, 2) * 100

            while gauge < temp:
                gauge += 1
                self.progressBar.setValue(gauge)

            i += 1
            downloader.browser.back()

        downloader.browser.close()