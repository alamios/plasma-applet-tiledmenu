# Plasma 6.6 migration

This independently maintained fork adapts Tiled Menu to Plasma 6.6.
The original project is https://github.com/Zren/plasma-applet-tiledmenu.

Baseline: Zren/plasma-applet-tiledmenu at `21c8540`, already using Plasma 6's
metadata.json and PlasmoidItem. Migration branch: `migration/plasma-6.6`; package version 46.1
is a development version, not an upstream release.

Target detected on 2026-10-10: Plasma desktop/workspace 6.6.6, Qt 6.10.2 and KDE
Frameworks 6.24. The minimum Plasma API stays 6.0; older Plasma 6 versions have
not been tested.

## Repository history

`upstream-baseline` is an annotated tag at the original upstream commit
`21c8540`. The two migration commits live on `migration/plasma-6.6` and are merged
into `main` with an explicit merge commit. This preserves the original base and
the migration as separate points in the local history. GitHub publication is
managed separately by the repository owner.

## Changes

* Add generated native cfg_* aliases and a local draft for General settings,
  so the standard Plasma Apply/OK/Cancel flow can handle edits. The existing
  layout import/export page still saves immediately.
* Restore the missing TextField used to configure terminal, task manager and
  file manager applications. Loading values does not write back to settings.
* Replace Qt Quick Controls 1 in the hidden advanced page with Qt 6 controls.
  Obtain defaults directly from the configuration property map; avoid local XML
  requests and removed plasmoid.file(). Lists remain read-only in this page.
* Route expansion changes through the root PlasmoidItem and pass it to the
  Kicker runner and the popup's appletInterface property.
* Initialize search focus when the full representation becomes available.
* Handle Enter when no search result is selected.
* Attach runner count/data subscriptions with lifecycle-managed Connections.
* Replace removed PlasmaCore.Theme references with Kirigami colors and use an
  explicit Flickable for Qt Quick Controls 2 tile scrolling and drag coordinates.
  The old Oxygen-specific color override is replaced by the active theme color.
* Replace a remaining deprecated Kirigami devicePixelRatio reference.
* Use Plasma 6 install/remove tools, correct removal by plugin ID, and keep
  restarting Plasma opt-in. Install failures stop the script.
* Allow local builds without extracting or merging translations.

## Validation

* All 77 package QML components resolve with the installed Qt 6/KDE modules.
* Generated configuration aliases match `config/main.xml`. Draft edits update
  cfg_* properties without modifying live settings in the test harness.
* Behavior checks exercise stored configuration loading, user edits, external
  updates, and closing search results/actions only when the runner requests it.
* `bash ./build --no-merge` compiles translation catalogs and builds a .plasmoid.
* Archive installation, script upgrade and script removal pass with isolated
  XDG data/config/cache directories in /tmp.
* `tools/check-runtime.py` loads an instrumented copy with plasmoidviewer:
  114 applications were listed, a real Konsole query returned results, native
  result actions and the context menu loaded, and a tile was added and its editor
  requested. General configuration opened without missing cfg_* warnings.
* Bash syntax checks and `git diff --check` pass.

`tools/check-qml.py` resolves types and runs a small mocked configuration/runner
harness. The separate `tools/check-runtime.py` runs a real preview containment, search
and context menu in an isolated temporary package and captures an offscreen
image. Neither check launches an application or tests real window-manager
interaction.
The installed plasmoidviewer desktop containment also logs its own
`isScreenUiReady` API error; isolated previews have no activity-history database.
These messages come from KDE’s host components, rather than this widget.
A SimpleKCM scene-placement warning occurs while opening the configuration.
Full logs and a screenshot are retained under the printed /tmp preview path.

## Manual checks

Run `plasmoidviewer -a "$PWD/package"` with Plasma 6's plasma-sdk. Then test a
real panel instance for activation/closing, searching and result context menus,
application launching, mouse-driven tile pinning/editing, file drops, import/export, panel
icon customization, keyboard shortcuts, popup resizing, high DPI and tiles-only
mode. Upstream v46 documented unfinished drag/drop, transitions, resizing and
other features; those require explicit runtime confirmation or further work.

After editing the KConfig schema, run `/usr/bin/python3 tools/generate-config.py`.
Use its `--check` option to detect stale configuration aliases.

## Upgrading a legacy Plasma 5 installation

Tiled Menu v45 can contain metadata.json with KPlugin.ServiceTypes and
X-Plasma-MainScript=ui/Main.qml, but without KPackageStructure. Plasma 6 can find
that metadata while rejecting an upgrade with “does not match requested format
Plasma/Applet”. Do not rely on `kpackagetool6 --show` to identify an upgradeable
local package.

`install` now invokes `tools/install-package.py`, which detects a legacy local
package, moves it into a timestamped backup under the XDG data directory, and
installs the new package under the same plugin ID. Installation failure restores
the original package. Existing panel configuration is not modified. Keep the
existing widget instance and log out and back in to reload it.

`tools/test-install.py` verifies recovery from v45 metadata, preservation of the
old package, repeated upgrade, removal, failure rollback, and byte-identical
synthetic panel settings in isolated XDG directories. The real v45 installation
reported on 2026-10-10 was successfully replaced and backed up. This verifies
package recovery; checking the user's complete existing tile layout after
reloading Plasma remains a manual step.

## Tile drag regression

The readonly `dragActive` property emits a change notification without a value
argument. Its old function(dragActive) handler tested an undefined argument and
never started the internal scene drag. TileItem now reads its own property and
uses Drag.Internal with the press hotspot. The mouse area retains its grab
against Flickable, and disabling drag smoothing avoids a cell-position offset
caused by the drag threshold. The grid rejects occupied/locked destinations,
accepts successful drops, and clears stale offsets on completion.

`tools/test-drag.py` sends real mouse events through a QQuickView containing the
production TileGrid and TileItem. It reproduces the unchanged-coordinate bug
before the fix and verifies moving a tile without launching an application,
rejecting occupied cells, honoring the tile lock, and canceling outside the grid.
Panel-specific interaction still needs confirmation after reloading the widget.
Qt drag API reference: https://doc.qt.io/qt-6/qml-qtquick-drag.html
