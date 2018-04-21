"""
A singleton to hold them all. I love mutating state.
"""
import pickle
from DataClasses import Application, View
class DataManagerDefinition:
    def __init__(self):
        self.is_on_app_menu=False
        self.applications = [] #list of applications
        self.actual_opened_view = None
        self.actual_opened_view_internal:View = None
        self.actual_application:Application= None #App object
    def save(self):
        with open("dataManager.pickle", "wb") as f:
            pickle.dump(self.applications, open("dataManager.pickle", "wb"))

    def load(self):
        try:
            with open("dataManager.pickle", "rb") as f:
               self.applications = pickle.load(f)
        except:
            self.applications = []
    def getAppByName(self, n:str)->Application:
        return [x for x in self.applications if x.name==n][0]
    def getAppBy(self,attr, value:str)->Application:
        l=exec("[x for x in self.applications if x.{0}=={1}][0]".format(attr,value))
        return l