import QtQuick
import "../package/contents/ui" as TiledMenu

Item {
    id: widget
    width: 600
    height: 400
    property alias grid: tileGrid
    property alias configuration: configuration
    property int launches: 0
    property string layout: JSON.stringify(tileGrid.tileModel)
    property var tileEditorView: null
    function i18n(text) { return text }
    function i18nc(context, text) { return text }
    property QtObject plasmoid: QtObject {
        property alias configuration: configuration
    }
    QtObject {
        id: configuration
        property bool tilesLocked: false
    }
    QtObject {
        id: config
        property color defaultTileColor: "steelblue"
        property bool defaultTileGradient: false
        property int groupLabelAlignment: Text.AlignLeft
        property int tileLabelAlignment: Text.AlignLeft
    }
    QtObject {
        id: appsModel
        property QtObject tileGridModel: QtObject {
            property var favorites: []
            function getApp(url) { return null }
            function runApp(url) { widget.launches++ }
        }
        property QtObject allAppsModel: QtObject {
            function hasApp(url) { return false }
        }
    }
    QtObject {
        id: logger
        function debug() {}
    }
    Item { id: popup }
    TiledMenu.TileGrid {
        id: tileGrid
        anchors.fill: parent
        cellSize: 60
        cellMargin: 0
        cellPushedMargin: 0
        tileModel: [
            {x: 0, y: 0, w: 2, h: 2, url: "test.desktop", label: "Move me"},
            {x: 4, y: 0, w: 2, h: 2, url: "other.desktop", label: "Occupied"}
        ]
    }
}
