fonts={1:"oswald.name", 2:"lato.name", 3:"roboto.name"}
from configurationFile import config
import Images
from copy import deepcopy
class Action:
    def __init__(self, name, callback_name, callback, extras):
        self.name=name
        self.callbackName = callback_name
        self.callback = callback
        self.extras = extras
    def get_as_json(self):
        return {
            "name":self.name,
            "callbackName":self.callbackName,
            "extras":self.extras
        }
    @staticmethod
    def makeFromList(l):
        def onExc(a,indx,defa):
            try:
                return a[indx]
            except KeyError:
                return defa

        return [Action(a["name"], a["callback"],None,onExc(a,"extras",'""')) for a in l ]

class View:
    def __init__(self, name, type, actions, properties,raw):
        self.name = name
        self.uses_templating = True
        self.type = type
        self.actions = actions
        self.properties = properties
        self.raw = raw
    def update(self, attrs:dict):
        def find_by_id(dic:dict,id:str)->dict:
            queue = [dic]
            for obj in queue:
                if "content" in obj:
                    queue+=obj["content"]
                if "id" in obj and obj["id"] == id:
                    return obj
        for new_attr,value in attrs.items():
            self.properties[new_attr] = value
    def toTemplatingSystem(self)->dict:
        def get_image_if_property_not_empty(property,asBg):
            try:
                return {"type":"image", "source":self.properties[property], "asBackground":asBg}
            except:
                return {"type":"item"}
        def get_actions_list(customProps={}):
            l=[]
            for action in self.actions:
                a=vars(action)
                del a["callback"]
                a["type"]="action"
                for key,value in customProps.items():
                    a[key]=value
                l.append(a)
            return l

        def text()->dict:
            a={
                    "datatype": "text",
                    "templateName": "text",
                    "layout": {
                        "absoluteWidth": 160,
                        "x": 0,
                        "y": 0,
                        "background": get_image_if_property_not_empty("image", True),
                        "content": [


                            {
                                "type": "verticalLayout",
                                "width": 1,

                                "marginTop": 5,
                                "VAlign":"top",
                                "content": [

                                    {
                                        "type": "rectangle",



                                        "content": [
                                            {
                                                "id":"significant",
                                                "type": "text",
                                                "width": 1,
                                                "text": self.properties["significant"],
                                                "fontNumber": 1,
                                                "fontSize":13,

                                                "textAlign": "center"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "rectangle",
                                        "width": 1,


                                        "content": [
                                            {
                                                "type": "text",
                                                "width": 1,
                                                "id": "minor",
                                                "text": self.properties["minor"],
                                                "fontNumber": 1
                                            }
                                        ]
                                    }

                                    ]+ get_actions_list({"width":1})

                            }

                                ]
                            }

                    }


            return a
        def music()->dict:
            return None
            return  {
                    "datatype": "media",
                    "templateName": "mediaPlayer",
                    "layout": {

                        "absoluteWidth": 160,
                        "x": 0,
                        "y": 0,
                        "background":get_image_if_property_not_empty("image", True),
                        "content": [

                            {
                                "type":"rectangle",
                                "color":"rgba(1,1,1,0.3)",

                                "content":[
                            {
                                "type": "verticalLayout",
                                "width": 1,

                               "spacing":0,

                                "content": [

                                    {
                                        "type": "rectangle",
                                        "width": 1,


                                        "content": [
                                            {
                                                "type": "text",
                                                "width": 1,
                                                "id":"song",
                                                "text": self.properties["song"],
                                                "fontNumber": 1,
                                                "fontSize":13,
                                                "VAlign": "center",
                                                "textAlign": "center"
                                            }
                                        ]
                                    },
                                    {
                                        "type": "rectangle",
                                        "width": 1,


                                        "content": [
                                            {
                                                "HAlign":"center",
                                                "id":"performer",
                                                "type": "text",
                                                "width": 1,
                                                "fontNumber":3,
                                                "text": self.properties["performer"],
                                                "fontNumber": 1
                                            }
                                        ]
                                    },
                                    {
                                      "type":"progressBar",
                                       "value":0.25,
                                        "absoluteHeight":25,

                                    },
                                    {
                                        "type":"horizontalLayout",
                                        "spacing":5,
                                        "width":0.9,
                                        "HAlign":"center",
                                        "content":get_actions_list()
                                    }
                                    ]}]}]}}
        def list()->dict:
            def get_list_data():
                #this is where the code started getting bad xdd
                if isinstance(self.properties["listData"][0], dict):
                    #if is a composed object, therefore a more complicated template
                    return self.properties["listData"]
                elif isinstance(self.properties["listData"][0], str):
                    #otherwise it is a simple list, transform to simple template
                    new_list_data = [{"text":{"text":x}} for x in self.properties["listData"]]
                    self.properties["listData"] = new_list_data


                return self.properties["listData"]
            def get_list_element_template():
                element_template = "default"
                if "listTemplate" in self.properties:
                    element_template = self.properties["listTemplate"]
                return element_template
            #list is transformed into list xd??
            return {
                "datatype": "list",
                "templateName": "listView",
                "layout": {
                    "absoluteWidth": 160,
                    "x": 0,
                    "y": 0,
                    "content": [
                        {
                        "type":"verticalLayout",
                            "spacing":5,
                         "listTemplate":get_list_element_template(),
                            "listData":get_list_data(),
                         "content":[]
                         }
                    ]
                }
            }




        router = {
            "text":text,
            "music":music,
            "list":list
        }
        in_templating = router[self.type]()
        return in_templating
    def toQML(self,templating:dict):
        HEADER = """
import QtQuick 2.7;
import QtQuick.Controls 2.0;
import QtQuick.Layouts 1.0;

        """
        indent=0
        out=""
        def convertAttributes(type, attrs)->dict:

            #typ już w QML
            print("============")
            print(type)

            try:
                attrs["width"] = "parent.width*" + str(attrs["width"])
            except:pass
            if type == "Root":
               attrs["height"] = config["screenY"]
               #is there a background?
               if "background" in attrs:
                    if attrs["background"]["type"] == "image":
                        path = Images.save_image_from_base64(attrs["background"]["source"], "img", "png", "apka")

                        attrs["backgroundImageSource"] = '"'+Images.add_protocol(path.replace('\\', '/'))+'"'
                    del attrs["background"]
            else:
                #delete id, mainly because of list template and id not being unique there.
                if "id" in attrs:
                    attrs["objectName"] = attrs["id"]
                    del attrs["id"]
            if type =="Action":
               attrs["callbackSignal"]="root.action"
            if type=="CustomListElement":
                attrs["callbackSignal"] ="root.listClick"
                attrs["height"] = "childrenRect.height"
            simple_changes = {"absoluteWidth":"width",
                              "absoluteHeight":"height",
                              "marginTop":"anchors.topMargin",
                              "backgroundColor":"color",
                              "padding":"anchors.margins",
                              "fontSize":"font.pointSize",
                              "marginLeft": "anchors.leftMargin",
                              "marginRight":"anchors.rightMargin",
                              "marginBottom": "anchors.bottomMargin",
                              "textAlign":"horizontalAlignment"
                              }
            simple_changes_values = {"center":"parent.horizontalCenter"}
            new_attrs = deepcopy(attrs)
            for key,value in attrs.items():
                new_attrs[key] = value
                if key in simple_changes:

                    new_key = simple_changes[key]
                    new_attrs[new_key] = value
                    del new_attrs[key]
            attrs = new_attrs
            for key,value in attrs.items():

                try:
                    if 'rgba(' in value:
                        colors = [float(x) for x in value.replace("rgba(","").replace(")","").split(",")]
                        new_attrs[key] = "Qt.rgba({0},{1},{2}, {3})".format(*colors)
                except TypeError:
                    pass

                       # attrs[simple_changes[key]] = simple_changes_values[attrs[simple_changes[key]]]
            if "HAlign" in attrs:
                changes_key = {"left":"anchors.left", "center":"anchors.horizontalCenter", "right":"anchors.right"}
                changes_value = {"left":"parent.left", "center":"parent.horizontalCenter", "right":"parent.right"}

                val = changes_value[attrs["HAlign"]]
                k = changes_key[attrs["HAlign"]]
                attrs[k] = val
                del attrs["HAlign"]
            if "VAlign" in attrs:
                changes_key = {"bottom": "anchors.bottom", "center": "anchors.verticalCenter", "top": "anchors.top"}
                changes_value = {"bottom": "parent.bottom", "center": "parent.verticalCenter", "top": "parent.top"}

                val = changes_value[attrs["VAlign"]]
                k = changes_key[attrs["VAlign"]]
                attrs[k] = val
                del attrs["VAlign"]



            if "horizontalAlignment" in attrs:
                changes = {"center":" Text.AlignCenter", "left":" Text.AlignLeft", "right":" Text.AlignRight"}
                attrs["horizontalAlignment"] = changes[attrs["horizontalAlignment"]]


           # Layout.preferredHeight: childrenRect.height
            #when there is no height specified implicitly, we should add:
            if "height" not in attrs and type in ["Rectangle", "Column", "Row"]:
                attrs["height"] = "childrenRect.height"
            #konwersja base64 na image

            if type == "Image":
                path = Images.save_image_from_base64(attrs["source"], "img", "png", "apka")

                attrs["source"] = Images.add_protocol(path.replace('\\','/'))
                if "asBackground" in attrs:
                    if attrs["asBackground"]:
                        attrs["x"]=0
                        attrs["y"]=0
                        attrs["height"] = config["screenY"]
                    else:
                        pass
                    del attrs["asBackground"]
            if type not in ["Action", "Text"]:
                if "width" not in attrs:
                    attrs["width"] = "parent.width"
                if "height" not in attrs:
                    attrs["height"] = "parent.height"

            if "fontNumber" in attrs:
                attrs["font.family"] = fonts[attrs["fontNumber"]]
                del attrs["fontNumber"]
            if "color" in attrs and "#" in attrs["color"]:
                attrs["color"]='"'+attrs["color"]+'"'
            if "color" not in attrs and type in ["Rectangle", "Root"]:
                attrs["color"]='"transparent"'
            if type=="Text":
                attrs["wrapMode"] = "Text.Wrap"
            if "listTemplate" in attrs and "listData" in attrs:
                #to jest lista!!
                if attrs["listTemplate"] == "default":
                    attrs["listTemplate"] = {
                        "type":"listItem",

                        "content":[
                            {"type":"text", "id":"text", "text":""}
                        ]
                    }
                def find_by_id(dic,id):
                    queue = dic["content"]
                    for item in queue:
                        print(item)
                        if "content" in item:
                            queue = queue + item["content"]
                        if "id" in item and item["id"] == id:
                            return item

                content = []
                template = attrs["listTemplate"]
                for index,actual_element in enumerate(attrs["listData"]):
                    element = deepcopy(template)
                    for id,value in actual_element.items():
                        to_be_changed = find_by_id(element, id)
                        for key,v in value.items():
                            to_be_changed[key] = v
                    element["extras"]='"'+str(index)+'"'
                    content.append(element)
                if "content" in attrs:
                    attrs["content"]+=content
                else:
                    attrs["content"]=content
                del attrs["listTemplate"]
                del attrs["listData"]





            return attrs

        def recursive(obj:dict):
            string_types=["text","name","callbackName", "source", "objectName"]

            nonlocal out
            nonlocal indent
            actual=""
            inner=""
            # tutaj konwersja atrybutów
            typ = "root"
            if "type" in obj:
                typ= obj["type"]
            obj2 = convertAttributes(types[typ],obj)

            for key, value in obj2.items():
                if key != "content":
                    if key == "type":
                        type = types[value]
                    else:
                        val = str(value)
                        if key in string_types:
                            val = '"'+val+'"'
                        inner+=" "*indent*4 + str(key)+":"+val+"\n"

            try:

                actual+=" "*indent*4 + type+"{\n"+inner
            except UnboundLocalError:
                actual += " "*indent*4 + "Root" + """{
                
                """+inner
            out+=actual
            if "content" in obj:
                for actualx in obj["content"]:
                    indent += 1
                    recursive(actualx)

            else:
                indent=0
            out+=" "*indent*4+"}\n"
        layout = templating["layout"]
        types = {"text":"Text", "rectangle":"Rectangle", "verticalLayout":"Column", "action":"Action", "horizontalLayout":"Row", "image":"Image", "progressBar":"ProgressBar", "item":"Item", "listItem":"CustomListElement", "root":"Root"}
        recursive(layout)
        out = HEADER+"\n"+out

        return out

class Application:
    def __init__(self, package, friendlyName, iconPath):
        self.package=package
        self.friendlyName = friendlyName
        self.iconPath = iconPath