#!/usr/bin/python3
"""Run a temporary instrumented applet in Plasma 6's plasmoidviewer."""
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

root = Path(__file__).resolve().parents[1]
preview = Path(tempfile.mkdtemp(prefix="tiledmenu-runtime-"))
package = preview / "package"
shutil.copytree(root / "package", package)
main = package / "contents/ui/main.qml"
source = main.read_text()
source = source.rstrip()[:-1] + '''
    Timer {
        interval: 1000
        running: true
        onTriggered: {
            widget.expanded = true
            search.query = "konsole"
        }
    }
    Timer {
        interval: 2500
        running: true
        onTriggered: {
            fullRepresentationItem.tileGrid.addApp("org.kde.konsole.desktop", 0, 0)
            console.log("SMOKE tile added", fullRepresentationItem.tileGrid.tileModel.length)
        }
    }
    Timer {
        interval: 8000
        running: true
        onTriggered: {
            fullRepresentationItem.tileGrid.editTile(fullRepresentationItem.tileGrid.tileModel[0])
            console.log("SMOKE tile editor requested")
        }
    }
    Timer {
        interval: 4500
        running: true
        onTriggered: {
            console.log("SMOKE apps", appsModel.allAppsModel.count, "results", search.results.count)
            if (search.results.count > 0) {
                console.log("SMOKE actions", JSON.stringify(search.results.getActionList(0)))
                var delegate = fullRepresentationItem.searchView.searchResultsView.listView.currentItem
                if (delegate) {
                    delegate.smokeContextMenu.open(2, 2)
                    console.log("SMOKE context menu opened")
                }
            }
            fullRepresentationItem.grabToImage(function(result) {
                result.saveToFile("SCREENSHOT_PATH")
            })
        }
    }
    Timer {
        interval: 6000
        running: true
        onTriggered: {
            Plasmoid.internalAction("configure").trigger()
            console.log("SMOKE configure requested")
        }
    }
}
'''.replace("SCREENSHOT_PATH", str(preview / "preview.png"))
main.write_text(source)
delegate = package / "contents/ui/MenuListItem.qml"
delegate.write_text(delegate.read_text().replace("id: itemDelegate", "id: itemDelegate\n    property alias smokeContextMenu: contextMenu", 1))
env = dict(os.environ, QT_QPA_PLATFORM="offscreen", KDE_DEBUG="1")
for key, directory in [("XDG_CONFIG_HOME", "config"), ("XDG_CACHE_HOME", "cache"), ("XDG_DATA_HOME", "data")]:
    env[key] = str(preview / directory)
command = ["plasmoidviewer", "-a", str(package), "-s", "1000x700"]
try:
    completed = subprocess.run(command, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=11)
    output = completed.stdout
    code = completed.returncode
except subprocess.TimeoutExpired as error:
    output = error.stdout or b""
    if isinstance(output, bytes):
        output = output.decode(errors="replace")
    code = 0  # A GUI preview normally stays open.
(preview / "runtime.log").write_text(output)
for line in output.splitlines():
    if "SMOKE" in line or str(package) in line:
        print(line)
print("Preview artifacts:", preview)
errors = [line for line in output.splitlines() if str(package) in line and ("Error:" in line or "is not defined" in line or "Unable to assign" in line or "Setting initial properties failed" in line)]
if errors or "SMOKE configure requested" not in output or "SMOKE context menu opened" not in output or "SMOKE tile editor requested" not in output:
    sys.exit(1)
sys.exit(bool(code))
