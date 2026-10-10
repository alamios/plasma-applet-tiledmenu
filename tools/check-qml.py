#!/usr/bin/python3
"""Resolve every QML component using the installed Qt 6 and KDE modules."""
import os
import sys
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
# Avoid crash dialogs on headless systems.
os.environ.setdefault("KDE_DEBUG", "1")
from PyQt6.QtCore import QUrl
from PyQt6.QtQml import QQmlComponent, QQmlEngine
from PyQt6.QtWidgets import QApplication

app = QApplication([])
engine = QQmlEngine()
paths = sorted((Path(__file__).resolve().parents[1] / "package/contents").rglob("*.qml"))
failed = 0
for path in paths:
    component = QQmlComponent(engine, QUrl.fromLocalFile(str(path)))
    if not component.isReady():
        failed += 1
        print(path)
        for error in component.errors():
            print(error.toString())
print(f"QML: {len(paths)} components checked, {failed} failed.")
regression = QQmlComponent(engine, QUrl.fromLocalFile(str(Path(__file__).with_name("Regression.qml").resolve())))
instance = regression.create() if regression.isReady() else None
if instance is None or instance.property("result") != "PASS":
    failed += 1
    print("Behavior checks failed:", instance.property("result") if instance else "cannot create harness")
    for error in regression.errors():
        print(error.toString())
else:
    print("Behavior checks: configuration edits and search activation passed.")
sys.exit(bool(failed))
