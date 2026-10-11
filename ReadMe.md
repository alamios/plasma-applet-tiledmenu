# Tiled Menu

Tiled Menu is an application launcher for **KDE Plasma 6.6**, inspired by the
Windows 10 Start Menu. This [independent fork](https://github.com/alamios/plasma-applet-tiledmenu)
provides configurable tiles, application search and sidebar shortcuts.

The current version is **46.2**. Versions are distributed as source code on
GitHub; build the installable widget locally using the instructions below.

## Features

- Pin applications, files and folders to a tile grid.
- Resize tiles, customize their labels, colors and background images.
- Rearrange tiles and move or sort labeled groups.
- Browse applications alphabetically or by category, and search with KRunner.
- Customize sidebar shortcuts and use a tiles-only view.
- Export and import the menu layout.

Tile groups are labeled areas of the grid; nested tile folders are not supported.

## Requirements

The validated environment is Plasma **6.6.6**, Qt **6.10.2** and KDE Frameworks
**6.24**. The widget uses Plasma 6 QML modules, including Kirigami, KSvg, Plasma
components, Kicker and Qt5Compat GraphicalEffects. It does not require a C++ build.
Python 3 and gettext are needed to build the package from source.

## Build and install

Run these commands from the repository root:

```bash
bash ./build --no-merge
bash ./install
```

The build compiles existing translations without changing their sources and
produces `tiledmenu-v46.2-plasma6-0.plasmoid`. The installer uses `kpackagetool6`
and installs or updates the widget for the current user.

For a new installation, add **Tiled Menu** using Plasma's widget picker. For an
update, keep the existing widget in its panel and log out and back in to reload
it. Removing and recreating the widget creates a new instance with separate
settings.

To restart Plasma explicitly on systems using its systemd user service:

```bash
bash ./install --restart
```

To remove the installed package:

```bash
bash ./uninstall
```

## Configuration and layout

Use the widget's settings to customize appearance, search, sidebar shortcuts and
application commands. General settings are saved with **Apply** or **OK**;
**Cancel** discards those edits. Layout import/export saves changes immediately.
Export your layout before importing a different one.

Pin an application from its context menu, or drag applications, files and folders
from Dolphin onto the grid. Use **Edit Tile** to set a label, icon, background,
position and size. Tile sizes are expressed in grid cells, such as 1×1, 2×2 or
4×2. Group labels provide actions to move and sort their tiles.

Drag an unlocked tile with the left mouse button onto an empty grid position.
Dropping over an occupied position or outside the grid leaves it in place.
Disable **Lock Tiles** in the context menu before rearranging tiles.
Use **Meta + right-button drag** to resize the menu with the default Plasma
window-management shortcut.

## Existing installations

The plugin ID is `com.github.zren.tiledmenu`, so updates reuse existing widget
settings. Access to files and applications still depends on their paths and
launcher identifiers being available on the system.

The installer handles older package formats by backing up the package under
`$XDG_DATA_HOME/tiledmenu/backups/`, normally `~/.local/share/tiledmenu/backups/`,
then installing the current package. If installation fails, it restores the old
package. It does not rewrite the panel configuration.

## Development and contributions

Report issues and submit changes to [this fork's repository](https://github.com/alamios/plasma-applet-tiledmenu).
Include the Plasma and Qt versions, reproduction steps and relevant QML errors.

- [Development and testing](DEVELOPMENT.md)
- [Theming](Theming.md)
- [Translations](package/translate/ReadMe.md)
- [Changelog](Changelog.md)

## Credits and license

Based on [Tiled Menu by Chris Holland (Zren)](https://github.com/Zren/plasma-applet-tiledmenu).
This fork is maintained independently. The package declares the **GPL-2.0-or-later**
license and retains the original author attribution.
