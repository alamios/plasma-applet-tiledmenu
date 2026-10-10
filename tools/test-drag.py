#!/usr/bin/python3
"""Exercise real pointer drags on the production TileGrid and TileItem."""
import json
import os
from pathlib import Path

os.environ.setdefault('QT_QPA_PLATFORM', 'offscreen')
os.environ.setdefault('KDE_DEBUG', '1')
from PyQt6.QtCore import QPoint, Qt, QUrl
from PyQt6.QtQuick import QQuickView
from PyQt6.QtTest import QTest
from PyQt6.QtWidgets import QApplication

app = QApplication([])
view = QQuickView()
view.setSource(QUrl.fromLocalFile(str(Path(__file__).with_name('DragRegression.qml').resolve())))
assert not view.errors(), '\n'.join(error.toString() for error in view.errors())
view.show()
QTest.qWait(100)
root = view.rootObject()

def layout():
    return json.loads(root.property('layout'))

def drag(start, end):
    QTest.mousePress(view, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, QPoint(*start))
    for step in range(1, 11):
        x = round(start[0] + (end[0] - start[0]) * step / 10)
        y = round(start[1] + (end[1] - start[1]) * step / 10)
        QTest.mouseMove(view, QPoint(x, y), 20)
    QTest.mouseRelease(view, Qt.MouseButton.LeftButton, Qt.KeyboardModifier.NoModifier, QPoint(*end))
    QTest.qWait(100)

drag((30, 30), (150, 150))
assert (layout()[0]['x'], layout()[0]['y']) == (2, 2), layout()
assert root.property('launches') == 0, 'Dragging launched an application'
print('PASS: real mouse drag moved a tile without launching it')

drag((150, 150), (270, 30))
assert (layout()[0]['x'], layout()[0]['y']) == (2, 2), 'Drop overlapped an occupied tile'
print('PASS: occupied destination leaves the tile in its original position')

root.property('configuration').setProperty('tilesLocked', True)
drag((150, 150), (30, 150))
assert (layout()[0]['x'], layout()[0]['y']) == (2, 2), 'Locked tile moved'
root.property('configuration').setProperty('tilesLocked', False)
print('PASS: locked tiles cannot be moved')

drag((150, 150), (700, 450))
assert (layout()[0]['x'], layout()[0]['y']) == (2, 2), 'Drop outside the grid moved the tile'
print('PASS: dropping outside the grid cancels the move')
