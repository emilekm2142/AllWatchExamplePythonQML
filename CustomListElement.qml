import QtQuick 2.7
Rectangle {
 FontLoader { id: oswald; source: "fonts/Oswald-Regular.ttf" }
  FontLoader { id: lato; source: "fonts/Lato-Regular.ttf" }
    FontLoader { id: roboto; source: "fonts/Roboto-Regular.ttf" }
    id:buttonRoot
    Behavior on color{
        ColorAnimation {
            duration: 100
        }
    }

    property string name
    property string callbackName
    property string extras:""
    property var callbackSignal
    property string buttonColor:"white"
    property string textColor:"white"
    color: buttonColor

    MouseArea{
        anchors.fill: parent
        onClicked: {

            callbackSignal(buttonRoot.extras);
        }
    }

}
