import sys
from PyQt4 import QtGui
from GUI.design import MainDialog
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from crawling.parser import Parser
from bs4 import BeautifulSoup
import time

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Dialog = MainDialog()
    Dialog.show()
    sys.exit(app.exec_())