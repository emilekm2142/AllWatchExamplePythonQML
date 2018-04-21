import QtQuick 2.7;
import QtQuick.Controls 2.0;
import QtQuick.Layouts 1.0;


Rectangle{
signal action(string callbackName)



                x:0
y:0
height:128
width:160
    Column{
    width:parent.width*1
    anchors.topMargin:5
    anchors.top:parent.top
    height:childrenRect.height
        Rectangle{
        width:parent.width*0.2
        height:childrenRect.height
        color:"transparent"
            Text{
            width:parent.width*1
            text:""
            font.pointSize:13
            horizontalAlignment: Text.AlignCenter
            anchors.verticalCenter:parent.verticalCenter
            font.family:roboto.name
}
}
    Rectangle{
    width:parent.width*0.7
    color:"#3F51B5"
    height:20
        Text{
        width:parent.width*1
        text:"I should buy some milk"
        font.family:oswald.name
}
}
    Rectangle{
signal action(string callbackName)



                    name:"ok"
    callbackName:"ok"
    extras:
    height:128
    width:parent.width
}
}
}