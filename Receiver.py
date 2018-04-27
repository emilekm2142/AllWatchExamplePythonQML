from PyQt5.QtCore import QUrl, QObject, QMetaObject,Qt,pyqtSlot, QThread, pyqtSignal
from time import sleep
import serial
from DataClasses import *
import json
from requests import *
#to send something from this module to the main thread, emit a signal
class ReceiverThread(QThread):
    __info_received_signal = pyqtSignal(object)
    __send_data_signal = pyqtSignal(object)

    windowInstance= None
    config = None
    interpreterInstance = None
    def send_data(self,data):
        self.__send_data_signal.emit(data)
    def __send_data(self,data):
        print(data)
    def receive_signal(self,info,delay):
        sleep(delay)
        try:
            in_json = json.loads(info)
        except:
            in_json = info
        self.__info_received_signal.emit(in_json)

    def run(self):
        self.__info_received_signal.connect(self.onLine)
        self.__send_data_signal.connect(self.__send_data)
        input()
        self.onLine(show_music_player)
        #self.onLine(install_notes_application)
        #input()
        #self.onLine(open_notes_screen_initial)
        input()
        self.onLine(update_music_player)
        input()
       # input()
        #self.onLine(open_note_screen)
        #input()
        for x in range(50):
            update_note_screen["data"]["minor"] = str(x)
            sleep(0.05)
            self.onLine(update_note_screen)
        if self.config["useBluetooth"]:
            with serial.Serial() as ser:
                ser.baudrate = 19200
                ser.port = 'COM1'
                ser.open()
                while True:
                    line = ser.readline()
                    self.onLine(line)
        else:
            while True:
                self.onLine(input())
    def onLine(self,info):
        if len(str(info))>5:
            print("onLine")
            try:
                in_json = json.loads(info)
            except:
                in_json = info
            self.interpreterInstance.Interpret(in_json)
