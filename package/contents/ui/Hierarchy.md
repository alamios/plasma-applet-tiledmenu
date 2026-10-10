# Plasma 6 component hierarchy

`widget` owns expansion and representation properties. `plasmoid.configuration`
continues to provide persistent settings. Both the root application model and
the search runner model use `widget` as their `appletInterface`.
`SearchModel` manages subscriptions to runner models with `Instantiator` and
`Connections`; `SearchResultsModel` flattens results and dispatches actions.
`TileGrid` uses an explicit Flickable inside ScrollView. General configuration
uses `ConfigForm`, whose cfg_* aliases are generated from `config/main.xml`.

main.qml (PlasmoidItem, id: widget)
	SearchModel
		SearchResultsModel
	LauncherIcon
	Popup
		SearchView
			SidebarView
			SearchResultsView
				SearchResultsList
			SearchField
		TileGrid


krunner_id (filename)

org.kde.activities (activityrunner)
Audio Player Control Runner (audioplayercontrol)
baloosearch (baloosearch)
bookmarks (bookmarks)
calculator (calculator)
unitconverter (converter)
org.kde.datetime (datetime)
Dictionary (dictionary)
Kill Runner (kill)
kwin (kwin)
locations (locations)
places (places)
Name=plasma-desktop (plasma)
PowerDevil (powerdevil)
services (services)
desktopsessions (sessions)
shell (shell)
Spell Checker (spellchecker)
webshortcuts (webshortcuts)
org.kde.windowedwidgets (windowedwidgets)
windows (windows)
