import QtQuick
import "../package/contents/ui" as TiledMenu
import "../package/contents/ui/libconfig" as LibConfig

Item {
    id: widget
    property bool expanded: true
    property alias plasmoid: applet
    property alias runnerModel: runners
    property string result: ""
    QtObject {
        id: applet
        property QtObject configuration: QtObject {
            property string terminalApp: "org.kde.konsole"
        }
    }
    QtObject {
        id: runners
        property bool closeRequested: true
        property string lastAction: ""
        function modelForRow(index) { return runners }
        function trigger(index, actionId, argument) {
            lastAction = actionId
            return closeRequested
        }
    }
    TiledMenu.SearchResultsModel { id: results }
    LibConfig.TextField {
        id: terminalField
        configKey: "terminalApp"
    }
    LibConfig.ConfigForm {
        id: configurationForm
        cfg_terminalApp: "stored-terminal"
    }
    Component.onCompleted: {
        if (configurationForm.settings.terminalApp !== "stored-terminal") {
            result = "Plasma initial configuration did not reach the draft"; return
        }
        configurationForm.settings.terminalApp = "draft-terminal"
        if (configurationForm.cfg_terminalApp !== "draft-terminal" || applet.configuration.terminalApp !== "org.kde.konsole") {
            result = "Draft configuration did not preserve cfg aliases or changed live settings"; return
        }
        if (terminalField.text !== "org.kde.konsole") {
            result = "TextField did not load the stored value"; return
        }
        terminalField.text = "org.kde.yakuake"
        terminalField.textEdited()
        if (applet.configuration.terminalApp !== "org.kde.yakuake") {
            result = "TextField did not save a user edit"; return
        }
        applet.configuration.terminalApp = "org.kde.konsole"
        if (terminalField.text !== "org.kde.konsole") {
            result = "TextField did not follow an external update"; return
        }
        results.append({runnerIndex: 0, runnerItemIndex: 0})
        results.triggerIndex(0)
        if (expanded) { result = "Launching a result did not close the menu"; return }
        expanded = true
        results.triggerIndexAction(0, "testAction", "argument")
        if (expanded || runners.lastAction !== "testAction") {
            result = "A search action did not close the menu or reach the runner"; return
        }
        expanded = true
        runners.closeRequested = false
        results.triggerIndex(0)
        if (!expanded) { result = "The menu closed despite the runner request"; return }
        result = "PASS"
    }
}
