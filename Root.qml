import QtQuick 2.7
import QtQuick.Controls 2.0
import QtQuick.Layouts 1.3
Rectangle{


height:childrenRect.height

Component.onCompleted:{


var l=createActions(actionsList);

console.log("dupa");
try{
bg.source = backgroundImageSource;
}
catch(e){

}
}
//signal action(string callbackName, string extras)
property var rootref
property string actionsList
function createActions(actionsLista){


    if (actionsLista){
   // console.log(actionsLista);
    //console.log(actionsList.length);
    actionsLista = JSON.parse(actionsLista);
    var l=[];
    var container = actionsContainer;
    for (var i =0; i<actionsLista.length;i++){
        var properties = actionsLista[i];
        console.log(properties);


        var component = Qt.createComponent("Action.qml");

        var action = component.createObject(container, {name:properties["name"], callbackName:properties["callbackName"], callbackSignal: rootref.action});
        //l.add(action);
    }
    return l
    }
}
property string backgroundImageSource:""

       Behavior on opacity {
            id:fadeAnimation
            NumberAnimation {
                //This specifies how long the animation takes
                duration: 1
                //This selects an easing curve to interpolate with, the default is Easing.Linear
                easing.type: Easing.InQuart

            }
        }
        opacity:1
}