from DataClasses import *
from copy import deepcopy
import Images
from ApplicationWindow import ApplicationWindow
class CommandsInterpreter():
    windowInstance:ApplicationWindow =None
    DataManagerInstance = None
    def __init__(self):
        print("parser module initailized")
    def Interpret(self,command:dict):

        router = {
            "application":self.application_install,
            "view":self.view,
            "updateView":self.update_view
        }

        router[command["type"]](command)



    def application_install(self,command):
        inner_data = command["data"]
        old_app =None
        try:
            old_app = self.DataManagerInstance.getAppBy('package', inner_data['package'])
        except:pass

        reinstall = False
        try:
            reinstall = inner_data["reinstall"]
        except:
            pass


        if old_app is not None and reinstall:
            self.DataManagerInstance.applications.remove(old_app)
        if old_app is not None and not reinstall:
            return
        #install there
        app=Application(
            inner_data["package"],
            inner_data["name"],
            Images.add_protocol(Images.save_image_from_base64(inner_data["icon"],"img","png","apka"))
        )
        self.DataManagerInstance.applications.append(app)
        self.DataManagerInstance.save()
        print("installed!!")



    def view(self,command):
        inner_data = command["data"]

        properties:dict = deepcopy(inner_data)
        try:
            del properties["name"]
        except:pass
        try:
            del properties["datatype"]
        except:
            pass
        try:
            del properties["actions"]
        except:
            pass
        actions =[]
        try:
            actions = inner_data["actions"]
        except:
            pass
        view_object = View(inner_data["name"], inner_data["datatype"],Action.makeFromList(actions),properties, inner_data)
        self.windowInstance.display_QML_from_string_signal.emit(view_object)

    def update_view(self, command):
        if self.DataManagerInstance.actual_opened_view is not None and self.DataManagerInstance.actual_opened_view_internal.name == command["data"]["name"]:
            inner_data = command["data"]
            properties: dict = deepcopy(inner_data)
            self.DataManagerInstance.actual_opened_view_internal.update(properties)
            self.windowInstance.update_QML_from_string_signal.emit(properties)