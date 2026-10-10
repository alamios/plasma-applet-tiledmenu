# Tiled Menu for Plasma 6.6

This is an independently maintained fork of
[Zren/plasma-applet-tiledmenu](https://github.com/Zren/plasma-applet-tiledmenu),
a launcher inspired by Windows 10's Start Menu. It includes compatibility fixes
for **KDE Plasma 6.6** and recovery of legacy installations.

The original project and its KDE Store listing are maintained by the upstream
author. This fork is developed separately and is not an official upstream release.
See the [original KDE Store listing](https://store.kde.org/p/2142716/) for the
upstream widget.

## Repository history

`main` contains this independent fork. The migration commits are developed on
`migration/plasma-6.6` and merged into `main` with a merge commit.
The annotated tag `upstream-baseline` marks the original upstream commit
`21c8540`, before this fork's changes.

* Supports:
    * Pin/Favourite apps/files through the context menu (or by dragging them from dolphin).
    * Resizing (permanently) the size of the menu by Meta + Right Clicking and dragging.
    * Any size tile 1x1, 2x2, 4x4, 4x2, 1x3, etc.
    * Easily edit the background image of a tile.
    * Customizable sidebar shortcuts.
    * Jump to Letter/Category (can also default to this view)
    * Defaulting to only showing the tiles.
    * Labeling Groups of Tiles + Move Groups of Tiles + Sorting items in the group
* Does not support (Win10):
    * Tile Groups ("Folders")

## Plasma 6.6 compatibility and installation

This fork starts from upstream commit `21c8540`, which already includes an initial
Plasma 6 port. It adds fixes for configuration, launcher APIs, tile scrolling, and updating legacy Plasma 5 installations without losing panel settings.

It has been tested on Plasma **6.6.6**, Qt **6.10.2** and KDE Frameworks **6.24**.
Package version: **46.1**. Compatibility with other Plasma versions has not been
verified.

```bash
bash ./build --no-merge
bash ./install
```

`--no-merge` compiles existing translations without rewriting `.po` sources.
The resulting package is `tiledmenu-v46.1-plasma6-0.plasmoid`.
`install` uses `kpackagetool6` and works from any directory. It does not restart
Plasma automatically. Reload an existing widget by logging out and back in, or
explicitly use `bash ./install --restart` on systems with the
`plasma-plasmashell.service` user service. Remove it with `bash ./uninstall`.

The plugin ID remains `com.github.zren.tiledmenu`, so upgrading replaces an
existing installation and preserves its settings. The installer detects legacy
Plasma 5 packages with missing KPackageStructure or an old ui/Main.qml entry
point. It moves the old package to `$XDG_DATA_HOME/tiledmenu/backups/` (normally
`~/.local/share/tiledmenu/backups/`) before installing the Plasma 6 package and
restores it if installation fails. It does not modify panel configuration.
Export the tile layout first if you already use Tiled Menu. Add the widget from
Plasma's widget picker only if there is no existing instance. Keep an existing widget
in its panel and reload it by logging out and back in.

For development checks and a separate preview window:

```bash
/usr/bin/python3 tools/check-qml.py
/usr/bin/python3 tools/check-runtime.py
/usr/bin/python3 tools/test-install.py
plasmoidviewer -a "$PWD/package"
```

General settings use Plasma’s Apply/OK/Cancel mechanism. The layout import/export
page retains upstream’s immediate-save behavior.

The component check requires the system PyQt6 QtQml and QtWidgets modules and
installed KDE QML modules; it uses Qt 6 offscreen. `plasmoidviewer` requires
Plasma 6's `plasma-sdk`. Packaging requires Python 3 and gettext (`msgfmt`);
no C++ build is needed. After changing `config/main.xml`, regenerate the
configuration aliases with `/usr/bin/python3 tools/generate-config.py`. Qt5Compat GraphicalEffects is still required.

See [MIGRATION.md](MIGRATION.md) for validation results and remaining manual
checks. Passing component checks does not establish full desktop compatibility.

## Screenshots

![](https://i.imgur.com/rf6dI9Q.png)

## Theming

Read the [theming guide](Theming.md) to develop Desktop/Icon Themes for this widget.

## Translating

See the [package/translate](package/translate) folder for instructions on translating.
