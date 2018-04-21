"""
Quick docs:
receiver has to have a reference to AppWindow
AppWindow has to have a reference to receiver to be able to send signals to it

DataManager holds everythin that ApplicationWindow should not.
Keep ApplicationWindow neutral to any state. Works on arguments only
except for handling the actions clicks

"""





import serial
import asyncio,sys
from configurationFile import config
from PyQt5.QtCore import QUrl, QObject, QMetaObject,Qt,pyqtSlot, QThread
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView
from time import sleep
from PyQt5.QtCore import pyqtSignal
from ApplicationWindow import ApplicationWindow
import Receiver, Parser
from DataClasses import *
from _thread import start_new_thread
from DataManager import DataManagerDefinition


DataManager = DataManagerDefinition()
DataManager.load()
app = ApplicationWindow()
#DataManager.applications.append("asfasf")
#DataManager.save()
#DataManager = DataManager.load()
#print(DataManager.applications)


parser = Parser.CommandsInterpreter()
parser.windowInstance = app
parser.DataManagerInstance = DataManager
receiverThread =Receiver.ReceiverThread()
receiverThread.interpreterInstance = parser
receiverThread.config=config
receiverThread.windowInstance = app
receiverThread.start()
#start_new_thread(receiverThread.receive_signal, ({"type":"test"},1))
app.sender_instance = receiverThread
app.dataManager = DataManager
#receiverThread.receive_signal({"type":"test"})
#this starts the window loop in the main thread
app.make_window()