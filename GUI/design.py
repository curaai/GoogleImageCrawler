# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
from crawling.crawler import Crawler
from crawling.parser import Parser
from crawling.filecontrol import Controller
from threading import Thread
import time

from PyQt4 import QtCore, QtGui
import PyQt4.uic


class MainDialog(QtGui.QDialog):
    def __init__(self, parent=None):
        super(MainDialog, self).__init__(parent)

        self.ui = PyQt4.uic.loadUi("GUI\design.ui", self)

        self.ui.dirSelect.clicked.connect(self.select_dir)
        self.ui.startCrawling.clicked.connect(lambda x: Thread(target=self.start_crawling()).start)

    def select_dir(self):
        self.dirPath = str(QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\',
                                                         QtGui.QFileDialog.ShowDirsOnly))

    def start_crawling(self):
        self.progressBar.setValue(0)

        self.keyword = self.keyword_edit.text().strip()
        widthScale = self.scale_width_edit.text()
        heightScale = self.scale_height_edit.text()
        self.limit = int(self.image_count_edit.text())

        c = Crawler(self.keyword, self.limit)
        controller = Controller(self.dirPath)
        p = Parser()

        c.init_browser()
        if widthScale and heightScale:
            c.set_size(widthScale, heightScale)

        downloadCount = 0
        gauge = 0
        while True:
            if downloadCount >= c.limit:
                break

            res = c.click_image(downloadCount)
            while res == -1:
                c.scroll_down()
                c.click_image(downloadCount)
            time.sleep(.5)

            url = p.get_image_url(c.browser.page_source)
            if url is None:
                continue

            data, fileFormat = p.download_image(url)
            controller.save_image(data, str(downloadCount), fileFormat)

            downloadCount += 1
            temp = round(downloadCount / c.limit, 2) * 100

            time.sleep(1)
            while gauge < temp:
                gauge += 0.001
                self.progressBar.setValue(gauge)

        c.browser.close()
