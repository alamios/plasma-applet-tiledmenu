# Plasma 6 theming

This branch targets Plasma 6.6. SVG frames use `org.kde.ksvg` and icons use
`Kirigami.Icon`; colors are obtained from `Kirigami.Theme`. The historical
`theme.backgroundColor` and `theme.buttonBackgroundColor` names below correspond
to `Kirigami.Theme.backgroundColor` and `Kirigami.Theme.buttonBackgroundColor`.
Qt5Compat GraphicalEffects remains a runtime dependency for outline effects.
The old Oxygen-only background override now follows the active Kirigami color.
Check both light and dark Plasma styles when testing changes.

Fair warning, I might look for `widgets/tilemenu.svg` in the future for a the tile background (normal/hover) + sidebar (closed/opened) + sidebar buttons (normal/hover/pressed). So don't get toooo comfortable since I'm still developing this widget.

## Desktop Theme .svgs

https://develop.kde.org/docs/plasma/theme/

* Sidebar / Power Menu
	* Background
		* Defaults to drawing `theme.backgroundColor` at 50% transparency when closed, and 0% transparency when open. It used to be black (`#000`) in older versions.
		* `widgets/frame.svg` prefix: `raised` Background
		* Note that `theme.backgroundColor` is drawn undrneath the svg when the sidebar is open since 90% of themes have a transparent image.
* App List
	* Items
		* `widgets/button.svg`
	* Scrollbar
		* `widgets/scrollbar.svg`
* Search Box
	* `widgets/lineedit.svg`


## Color Theme

* `theme.backgroundColor` 
	* Drawn under the sidebar background svg when using the desktop theme.
* `theme.buttonBackgroundColor`
	* The default tile background color.


## Icons

* Sidebar
	* `open-menu-symbolic` Menu
	* `view-sort-ascending-symbolic` Apps
	* `system-search-symbolic` Search
	* `open-menu-symbolic` Menu
	* ...
	* `folder-open-symbolic` File Manager
	* `configure` Settings
	* `system-shutdown-symbolic` Power
		* `system-lock-screen` Lock
		* `system-log-out` Logout
		* `system-save-session` Save Session
		* `system-switch-user` Switch User
		* `system-suspend` Suspend
		* `system-suspend-hibernate` Hibernate
		* `system-reboot` Reboot
		* `system-shutdown` Shutdown
* Search View
	* Filter Bar
		* `system-search-symbolic` All/Default Filter
		* `window` Apps Filter
		* `document-new` File Filter
		* `globe` Bookmarks Filter

