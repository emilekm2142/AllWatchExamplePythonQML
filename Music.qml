import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
Root{
x:0
y:0
id:mroot
property string song
property int progress
property string performer
property string value


  Rectangle{

        id: rectangle
        anchors.fill:parent
        color:Qt.rgba(0,0,0,0.3)
    }
    Column{
        id: column

        anchors.bottom: parent.bottom
        height: childrenRect.height


        width: root.width
        Text{
            objectName:"performer"
            text:performer
            color:"white"
            font.family: oswald.name
            font.pointSize:8
            anchors.left: parent.left
            anchors.leftMargin: 8
        }

        Text{
            objectName:"song"
            text:song
            color:"white"
            font.family: oswald.name
            font.pointSize: 12
            anchors.left: parent.left
            anchors.leftMargin: 8
        }

        Rectangle {
            id: rectangle1
            height: 45
            color: Qt.rgba(1,1,1,0.3)
            anchors.left: parent.left
            anchors.leftMargin: 0
            anchors.right: parent.right
            anchors.rightMargin: 0
            Column{
                anchors.fill:parent
                Row{
                    id:actionsContainer
                    height: 27
                    spacing:5
                    width: root.width
                    objectName: "actionsContainer"

                }

                Slider {
                    Behavior on value{
                    NumberAnimation{
                    duration:100
                    }
                    }
                    id: control
                    value: progress
                    height: 5
                    width: root.width
                    background: Rectangle {
                        x: control.leftPadding
                        y: control.topPadding + control.availableHeight / 2 - height / 2
                        implicitWidth: 200
                        implicitHeight: 4
                        width: control.availableWidth
                        height: implicitHeight
                        radius: 2
                        color: "#bdbebf"

                        Rectangle {
                            width: control.visualPosition * parent.width
                            height: parent.height
                            color: "#21be2b"
                            radius: 2
                        }
                    }

                    handle: Rectangle {
                        x: control.leftPadding + control.visualPosition * (control.availableWidth - width)
                        y: control.topPadding + control.availableHeight / 2 - height / 2
                        implicitWidth: 12
                        implicitHeight: 12
                        radius: 10
                        color: control.pressed ? "#f0f0f0" : "#f6f6f6"
                        border.color: "#bdbebf"
                    }
                }

            }
        }

       }
}