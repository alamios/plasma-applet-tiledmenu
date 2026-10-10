import QtQuick
import QtQuick.Controls as QQC2
import QtQuick.Layouts
import org.kde.kirigami as Kirigami

QQC2.ScrollView {
    id: page
    clip: true
    contentWidth: availableWidth

    ListView {
        id: configTable
        spacing: Kirigami.Units.smallSpacing
        model: plasmoid.configuration.keys().filter(function(key) {
            return !key.endsWith("Default")
        }).sort()

        delegate: RowLayout {
            id: row
            required property string modelData
            width: configTable.width
            readonly property var configValue: plasmoid.configuration[modelData]
            readonly property var defaultValue: plasmoid.configuration[modelData + "Default"]

            QQC2.Label {
                text: row.modelData
                Layout.preferredWidth: 200
                wrapMode: Text.Wrap
                font.bold: JSON.stringify(row.configValue) !== JSON.stringify(row.defaultValue)
            }
            Loader {
                Layout.fillWidth: true
                sourceComponent: typeof row.configValue === "boolean" ? boolControl : textControl
            }
            Component {
                id: boolControl
                QQC2.CheckBox {
                    checked: row.configValue
                    onClicked: plasmoid.configuration[row.modelData] = checked
                }
            }
            Component {
                id: textControl
                QQC2.TextField {
                    text: typeof row.configValue === "object" ? JSON.stringify(row.configValue) : String(row.configValue)
                    // Lists remain read-only; the normal configuration pages edit them.
                    readOnly: typeof row.configValue === "object"
                    onEditingFinished: {
                        if (typeof row.configValue === "number") {
                            var number = Number(text)
                            if (text.trim() && isFinite(number)) {
                                plasmoid.configuration[row.modelData] = number
                            } else {
                                text = String(row.configValue)
                            }
                        } else if (!readOnly) {
                            plasmoid.configuration[row.modelData] = text
                        }
                    }
                }
            }
        }
    }
}
