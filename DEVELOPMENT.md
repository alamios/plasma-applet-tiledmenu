# Development

## Repository and package

`main` contains the maintained fork. Use feature branches for subsequent changes.
The tag `upstream-baseline` preserves the original project before the fork's
changes.

The installable package lives in `package/`. Its identity and version are in
`package/metadata.json`; persistent settings are defined in
`package/contents/config/main.xml`. Keep the plugin ID unchanged when updating
existing installations.

## Component structure

```text
main.qml (PlasmoidItem)
├── AppsModel
├── SearchModel → SearchResultsModel
├── AppletConfig
├── LauncherIcon
└── Popup
    ├── SidebarView
    ├── SearchView
    │   ├── AppsView
    │   ├── JumpToLetterView
    │   ├── SearchResultsView → SearchResultsList
    │   ├── SearchField
    │   └── TileEditorView (loaded on demand)
    └── TileGrid → TileItem → TileItemView
```

The root `widget` owns expansion and representation properties. Kicker models
receive it as their `appletInterface`. `SearchModel` manages runner subscriptions
with `Instantiator` and `Connections`; `SearchResultsModel` dispatches results
and their actions.

`TileGrid` uses a Flickable for scrolling and internal Qt Quick drags for tile
movement. Drag handlers read the current settings and account for the press
position and scroll offset, and commit only valid drops. General configuration edits a local
draft exposed through `cfg_*` aliases. Layout import/export writes directly to
the persistent configuration.

## Configuration schema

After changing `package/contents/config/main.xml`, regenerate its QML aliases:

```bash
/usr/bin/python3 tools/generate-config.py
/usr/bin/python3 tools/generate-config.py --check
```

`ConfigForm.qml` is generated; edit the schema rather than this file.

## Checks

The Python checks use the system PyQt6 QtQml, QtQuick, QtWidgets and QtTest modules
with the installed KDE QML modules. The runtime preview additionally requires
Plasma 6's `plasma-sdk`, which supplies `plasmoidviewer`, and Konsole for its
application-search scenario.

Run from the repository root:

```bash
/usr/bin/python3 tools/check-qml.py
/usr/bin/python3 tools/test-drag.py
/usr/bin/python3 tools/test-install.py
/usr/bin/python3 tools/check-runtime.py
/usr/bin/python3 tools/generate-config.py --check
bash -n build install uninstall
git diff --check
```

| Check | Coverage |
| --- | --- |
| `check-qml.py` | QML type resolution, configuration drafts and search activation with mocked runners |
| `test-drag.py` | Real mouse events for tile movement, occupied cells, locking and cancellation |
| `test-install.py` | Isolated install/upgrade/remove, older-package backup, rollback and unchanged panel settings |
| `check-runtime.py` | Real search, context menu, tile creation, editor and settings in a temporary preview |

The runtime check stores its log and screenshot in the temporary directory it
prints. Its isolated configuration has no activity-history database. Offscreen
previews may emit messages from KDE host components; consult the log to
distinguish them from errors in the widget. Automated checks do not replace
interaction with a real panel.

For an interactive preview:

```bash
plasmoidviewer -a "$PWD/package"
```

Before accepting UI changes, check activation and keyboard navigation, search
and context menus, internal and external drag/drop, resizing, scaling,
configuration cancellation, import/export and persistence after a session
restart. Use both light and dark themes.

## Packaging

```bash
bash ./build --no-merge
```

The filename uses the version in metadata.json and the current packaging suffix
`plasma6-0`; this suffix is not a claim that Plasma 6.0 has been tested.
Update [Changelog.md](Changelog.md) when behavior changes. For translation updates,
follow the [translation workflow](package/translate/ReadMe.md) before packaging.
