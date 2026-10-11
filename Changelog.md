# Changelog

## Unreleased

- Complete the Spanish catalog, including the application-command settings, and
  correct the URL and layout labels.
- Preserve the maintained translation guide when refreshing catalogs; print
  coverage in the terminal instead.

## 46.1

Initial maintained version of the independent Plasma 6.6 fork.

- Adapt launcher expansion, popup initialization and Kicker integration to the
  current Plasma APIs.
- Restore application-command settings and integrate General configuration with
  Apply, OK and Cancel using generated configuration aliases.
- Use Qt 6 controls and theme colors, with explicit scrolling for the tile grid.
- Restore tile dragging, including press offsets, collision rejection, locking
  and cancellation outside the grid.
- Handle an empty search selection and manage runner signal subscriptions with
  their object lifetime.
- Support older-package replacement with backup and rollback while retaining
  panel settings.
- Make Plasma restarts an explicit installation option and remove packages by
  plugin ID.
- Build packages without rewriting translation catalogs.
- Add component, runtime, pointer-drag and installation regression checks.

The original project's history is preserved in Git at `upstream-baseline`.
