from PyQt5.QtCore import QUrl, QObject, QMetaObject,Qt,pyqtSlot, QThread,pyqtSignal
from PyQt5.QtWidgets import QApplication
from PyQt5.QtQuick import QQuickView
import sys
from time import sleep
import json
from DataManager import DataManagerDefinition
from Receiver import ReceiverThread
from DataClasses import *
from viewToQML import *
from requests import *

class ApplicationWindow(QObject):
    sender_instance:ReceiverThread = None
    dataManager=None

    display_QML_from_string_signal= pyqtSignal(object)
    update_QML_from_string_signal = pyqtSignal(object)

    update_object_signal = pyqtSignal(object, object,object)

    #signals to be sent from parser
    show_view = pyqtSignal(object) #takes view



    def update_object(self, obj, key,value):
        obj.setProperty(key,value)
    def __init__(self):
        QObject.__init__(self)
        self.actual_screen= None

        self.show_view.connect(self.__show_view)
        self.display_QML_from_string_signal.connect(self.display_View)
        self.update_object_signal.connect(self.update_object)
        self.update_QML_from_string_signal.connect(self.update_view)
    def __show_view(self, view:View):
        #convert from object type to a QML
        view.toQML(self.root)
    def make_window(self):
        self.appObject = QApplication(sys.argv)
        self.appView = QQuickView()
        self.appView.setSource(QUrl("main.qml"))
        self.appView.show()
        self.root = self.appView.rootObject().findChild(object, "root")
        self.root.openApp.connect(self.open_application_callback)
        self.root.action.connect(self.callback_callback)
        self.root.listClick.connect(self.list_click)
        self.root.goBack.connect(self.goBack)
        self.display_main_screen()
        timeIndicator = self.appView.rootObject().findChild(object, "timeIndicator")
        class timeThread(QThread):
            timeIndicator=None
            dataManager = None
            updatesignal=None
            def run(self):
                while True:
                    sleep(0.2)
                    self.dataManager.update_time()
                    self.updatesignal.emit(self.timeIndicator, "text", self.dataManager.time)
                    #self.timeIndicator.setProperty("text", self.dataManager.time)
        timer = timeThread()
        timer.timeIndicator=timeIndicator
        timer.dataManager=self.dataManager
        timer.updatesignal = self.update_object_signal
        timer.start()



        self.appObject.exec_()
        sys.exit()

    """Receives already updated view. Current implementation does not update but rather destroy and rebuild ^^ xd"""
    def update_view(self, properties:dict):
        if self.dataManager.actual_opened_view is not None and self.dataManager.actual_opened_view_internal.name == properties["name"]:
            if self.dataManager.actual_opened_view_internal.uses_templating:
                for key,value in properties.items():
                    #print(key)
                    item = self.root.findChild(object, key)
                    if item is not None:
                        print(key)
                        print(value)
                        item.setProperty("text",value)
                    else:
                        print("no object named: ", key)
            else:
                for key, value in properties.items():
                    self.dataManager.actual_opened_view.setProperty(key,value)
            #self.root.destroyScreen(self.dataManager.actual_opened_view)
            #self.display_View(updated)

    def display_View(self, view:View):
        if self.dataManager.actual_opened_view is not None:
            self.root.destroyScreen(self.dataManager.actual_opened_view)
        templating = view.toTemplatingSystem()
        if templating is None:
            #it returned none, so we know that this template is not going to be made using the templating system but rathaer a native QML implementation
            templateName = view.type.title()
            actions_json = [ a.get_as_json() for a in view.actions]
            #view.properties["action"] = "root.test"
            #image
            path=None
            if "image" in view.properties:
                path = Images.save_image_from_base64(view.properties["image"], "img", "png", "apka")
                view.properties["backgroundImageSource"] =  Images.add_protocol(path.replace('\\', '/'))

            #print(actions_json)
            view.properties["actionsList"] = json.dumps(actions_json)
            view.properties["objectName"] = '"{0}"'.format(view.name)
            properties = json.dumps(view.properties)
            view.uses_templating=False
            self.dataManager.actual_opened_view_internal = view
            self.dataManager.actual_opened_view = self.root.makeScreenFromAQmlFile(templateName, properties)
        else:
            qml = view.toQML(templating)
            print(qml)

            self.dataManager.actual_opened_view_internal = view
            self.dataManager.actual_opened_view=self.root.makeScreen(qml)
    def display_main_screen(self):
        self.dataManager.is_on_app_menu=True
        view = View("mainScreen","list", [],{"listData":[x.friendlyName for x in self.dataManager.applications]},"")
        try:
            self.display_View(view)
        except IndexError:
            print("no apps")
    def open_application_callback(self,package):
        print("app!")
        print(id)

        self.dataManager.actual_application = [x for x in self.dataManager.applications if x.package == package][0]
        self.sender_instance.send_data(
        {
        "type":"dataRequest",
          "data":{
        "type":"applicationInitialScreen",
        "package":self.dataManager.actual_application.package,
        "friendlyName":self.dataManager.actual_application.friendlyName
        }})
    def list_click(self,id,extras):
        if self.dataManager.is_on_app_menu:
            try:
                self.open_application_callback(self.dataManager.applications[int(id)].package)
                self.dataManager.is_on_app_menu=False
            except IndexError:
                print("no such app!")
        else:
            app: Application = self.dataManager.actual_application
            self.sender_instance.send_data(json.dumps({
                "type": "listViewClick",
                "targetPackage": app.package,
                "friendlyName": app.friendlyName,
                "data": {
                    "id": id,
                    "extras": '"{0}"'.format(extras)


                }
            }))
        print(id,extras)
    def goBack(self,extra):
        app: Application = self.dataManager.actual_application
        try:
            self.sender_instance.send_data(json.dumps({
                "type": "systemAction",
                "targetPackage": app.package,
                "friendlyName": app.friendlyName,
                "data": {
                    "actionName": "back",
                    "screen": self.dataManager.actual_opened_view_internal.name


                }
            }))
        except AttributeError:
            pass
    def callback_callback(self,obj,e):
        app:Application = self.dataManager.actual_application
        self.sender_instance.send_data(json.dumps({
        "type":"action",
        "targetPackage":app.package,
        "friendlyName":app.friendlyName,
        "data":{
            "callbackName":obj,
            "name":obj,
            "extras":e

        }
        }))