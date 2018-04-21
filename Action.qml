import QtQuick 2.7
Rectangle {
 FontLoader { id: oswald; source: "fonts/Oswald-Regular.ttf" }
  FontLoader { id: lato; source: "fonts/Lato-Regular.ttf" }
    FontLoader { id: roboto; source: "fonts/Roboto-Regular.ttf" }

    height: childrenRect.height+4
    width:childrenRect.width+4
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
    property string buttonColor:"#9E9E9E"
    property string textColor:"white"
    property int textSize:8
    color: buttonColor
    Text{
        anchors.verticalCenter: parent.verticalCenter
        text:parent.name
        color:textColor
        anchors.horizontalCenter: parent.horizontalCenter
        verticalAlignment: Text.AlignVCenter
        horizontalAlignment: Text.AlignHCenter
        font.family:oswald.name
         font.pointSize: textSize

    }
    MouseArea{
        anchors.fill: parent
        onClicked: {

            callbackSignal(buttonRoot.callbackName, buttonRoot.extras);
        }
    }

}
