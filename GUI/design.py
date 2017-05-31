# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!
from crawling.crawler import Crawler
from crawling.parser import Parser

from PyQt4 import QtCore, QtGui

from bs4 import BeautifulSoup

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def __init__(self):
        self.dirPath = ""

    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(325, 307)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 20, 311, 281))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))

        self.insertLabel = QtGui.QLabel(self.groupBox_2)
        self.insertLabel.setGeometry(QtCore.QRect(20, 30, 91, 21))
        self.insertLabel.setObjectName(_fromUtf8("insertLabel"))

        self.startCrawling = QtGui.QPushButton(self.groupBox_2)
        self.startCrawling.setGeometry(QtCore.QRect(110, 200, 191, 21))
        self.startCrawling.setObjectName(_fromUtf8("startCrawling"))
        # 버튼을 누르면 crawling이 시작됨
        self.startCrawling.clicked.connect(self.start_crawling)

        self.setScale = QtGui.QLabel(self.groupBox_2)
        self.setScale.setGeometry(QtCore.QRect(10, 130, 71, 21))
        self.setScale.setObjectName(_fromUtf8("setScale"))

        self.scaleHeightEdit = QtGui.QTextEdit(self.groupBox_2)
        self.scaleHeightEdit.setGeometry(QtCore.QRect(80, 120, 71, 31))
        self.scaleHeightEdit.setObjectName(_fromUtf8("scaleHeightEdit"))
        self.scaleWidthEdit = QtGui.QTextEdit(self.groupBox_2)
        self.scaleWidthEdit.setGeometry(QtCore.QRect(200, 120, 71, 31))
        self.scaleWidthEdit.setObjectName(_fromUtf8("scaleWidthEdit"))

        self.alphabetX = QtGui.QLabel(self.groupBox_2)
        self.alphabetX.setGeometry(QtCore.QRect(170, 130, 21, 16))
        self.alphabetX.setObjectName(_fromUtf8("alphabetX"))

        self.keywordEdit = QtGui.QTextEdit(self.groupBox_2)
        self.keywordEdit.setGeometry(QtCore.QRect(100, 30, 141, 31))
        self.keywordEdit.setObjectName(_fromUtf8("keywordEdit"))

        self.countInsertLabel = QtGui.QLabel(self.groupBox_2)
        self.countInsertLabel.setGeometry(QtCore.QRect(20, 80, 91, 21))
        self.countInsertLabel.setObjectName(_fromUtf8("countInsertLabel"))

        self.limitEdit = QtGui.QTextEdit(self.groupBox_2)
        self.limitEdit.setGeometry(QtCore.QRect(140, 80, 71, 31))
        self.limitEdit.setObjectName(_fromUtf8("scaleWidthEdit_2"))

        self.progressBar = QtGui.QProgressBar(self.groupBox_2)
        self.progressBar.setGeometry(QtCore.QRect(30, 240, 271, 31))
        self.progressBar.setProperty("value", 0)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))

        self.label = QtGui.QLabel(self.groupBox_2)
        self.label.setGeometry(QtCore.QRect(20, 160, 271, 16))
        self.label.setObjectName(_fromUtf8("label"))

        self.dirSelect = QtGui.QPushButton(self.groupBox_2)
        self.dirSelect.setGeometry(QtCore.QRect(10, 200, 91, 23))
        self.dirSelect.setObjectName(_fromUtf8("dirSelect"))
        self.dirSelect.clicked.connect(self.selectDir)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.groupBox_2.setTitle(_translate("Dialog", "", None))
        self.insertLabel.setText(_translate("Dialog", "검색어 입력", None))
        self.startCrawling.setText(_translate("Dialog", "이미지 검색 시작", None))
        self.setScale.setText(_translate("Dialog", "크기 지정", None))
        self.alphabetX.setText(_translate("Dialog", "X", None))
        self.countInsertLabel.setText(_translate("Dialog", "이미지 개수 입력", None))
        self.label.setText(_translate("Dialog", "위 칸에 안적으면 모든 사이즈를 다운로드 합니다.", None))
        self.dirSelect.setText(_translate("Dialog", "저장 폴더 선택", None))

    def selectDir(self):
        self.dirPath = str(QtGui.QFileDialog.getExistingDirectory(None, 'Select a folder:', 'C:\\',
                                                         QtGui.QFileDialog.ShowDirsOnly))

    def start_crawling(self):
        self.progressBar.setValue(0)

        self.keyword = self.keywordEdit.toPlainText().strip()
        widthScale = self.scaleWidthEdit.toPlainText()
        heightScale = self.scaleHeightEdit.toPlainText()
        self.limit = int(self.limitEdit.toPlainText())

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
                gauge += 0.0001
                self.progressBar.setValue(gauge)

            i += 1
            downloader.browser.back()

        downloader.browser.close()