from PyQt5.QtCore import QUrl, QObject, QMetaObject,Qt,pyqtSlot, QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView
import sys
from time import sleep
from DataClasses import *
from viewToQML import *




appObject = QApplication(sys.argv)
appView = QQuickView()
appView.setSource(QUrl("Music.qml"))
appView.show()

appObject.exec_()
sys.exit()
