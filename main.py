import sys
from PyQt4 import QtGui
from GUI.design import MainDialog


if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    Dialog = MainDialog()
    Dialog.show()
    sys.exit(app.exec_())