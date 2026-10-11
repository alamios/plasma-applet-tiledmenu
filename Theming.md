# Theming

Tiled Menu uses Plasma style assets through `org.kde.ksvg`, icons through
`Kirigami.Icon`, and colors through `Kirigami.Theme`.

## Colors and backgrounds

The default tile background and sidebar color use `Kirigami.Theme.backgroundColor`.
Highlight and text effects use `Kirigami.Theme.highlightColor` and
`Kirigami.Theme.textColor`. User-selected colors override the corresponding
configuration defaults. Each tile can have its own background color, gradient
or image.

When style-based sidebar backgrounds are enabled, the sidebar draws the theme
color beneath `widgets/frame` with the `raised` prefix. The application button
style uses `widgets/button` with the `normal` and `pressed` prefixes. Qt Quick
and Plasma controls provide their own styling for text fields and scrollbars.

## Icons

Icons are resolved through the active icon theme. Common names include:

| Area | Icon names |
| --- | --- |
| Menu navigation | `open-menu-symbolic`, `view-sort-ascending-symbolic`, `system-search-symbolic` |
| Sidebar shortcuts | `folder-open-symbolic`, `configure`, `system-shutdown-symbolic` |
| Search filters | `window`, `document-new` |
| Session actions | `system-lock-screen`, `system-log-out`, `system-switch-user` |
| Power actions | `system-suspend`, `system-reboot`, `system-shutdown` |

Available session and power actions depend on the system. Custom tiles and the
panel launcher can use a selected icon or image.

## Validation

Check readable labels, icon contrast, hover/pressed effects, gradients and custom
background images in light and dark themes and at different display scales.
Outline effects require Qt5Compat GraphicalEffects.
