import QtQuick
import QtQuick.Controls as QQC2
import QtQuick.Layouts

QQC2.TextField {
    id: textField
    property string configKey: ""
    readonly property string configValue: configKey ? plasmoid.configuration[configKey] : ""

    Layout.fillWidth: true
    text: configValue

    // Save only user edits; loading the page must preserve the stored value.
    onTextEdited: {
        if (configKey && text !== configValue) {
            plasmoid.configuration[configKey] = text
        }
    }
    onConfigValueChanged: {
        if (text !== configValue) {
            text = configValue
        }
    }
}
