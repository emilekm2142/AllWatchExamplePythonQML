import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
Item{

width:160
height:128-topBar.height
Image{
id:bg
objectName:"bg"
height:128-topBar.height
width:160
}
Flickable{
 FontLoader { id: oswald; source: "fonts/Oswald-Regular.ttf" }
  FontLoader { id: lato; source: "fonts/Lato-Regular.ttf" }
    FontLoader { id: roboto; source: "fonts/Roboto-Regular.ttf" }
    function destroyScreen(screen){


   screen.destroy();

   }
   function destroyScreenTransition(screen){

   var delay=0;
   try{
    screen.opacity =0;
    delay=400;
   }
   catch(e){}
   screen.destroy(delay);

   }
  function makeScreen(str){
  var newObject = Qt.createQmlObject(str,
                                   root.contentItem,
                                   "dynamicSnippet1");
 //newObject.fadeAnimation.enabled=false;
newObject.opacity=1
return newObject;
  }
  function makeScreenFromAQmlFile(templateName, properties){
    var component = Qt.createComponent(templateName+".qml");
    var props = JSON.parse(properties);
    props["rootref"] = root;

    var sprite = component.createObject(root.contentItem, props);

    return sprite;
  }
function makeScreenTransition(str){

var newObject = Qt.createQmlObject(str,
                                   root.contentItem,
                                   "dynamicSnippet1");

newObject.opacity=1
return newObject;

}
function test(a,a){
console.log("come");
}
signal action(string callbackName, string extras)
signal openApp(string packageName)
signal listClick(int id, string extras)
signal goBack(string extras)
x:0
objectName:"root"
y:topBar.height


contentWidth: 160
 contentHeight: childrenRect.height
 height:128
id:root
width:160
 ScrollBar.vertical: ScrollBar {
        parent: parent.parent
        anchors.top: parent.top
        anchors.left: parent.right
        anchors.bottom: parent.bottom
    }
}
Rectangle{
id:topBar
    anchors.top:parent.top
    width:160
    height:20
    color:"#3F51B5"
    RowLayout{
    spacing:40

        Text{
        anchors.verticalCenter : parent.verticalCenter
           color:"white"
           font.family: oswald.name
        text:"<- Back"
        MouseArea{
            anchors.fill: parent
            onClicked: {

                root.goBack("");
            }
        }
        }
        Text{
        anchors.verticalCenter : parent.verticalCenter
        Layout.fillWidth: true
        horizontalAlignment: Text.AlignRight
           color:"white"
           font.family: oswald.name
        text:"15:31"
        objectName:"timeIndicator"
        }

    }
    }
}
