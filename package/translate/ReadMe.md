# Translations

Translation sources are the `.po` catalogs in this directory. `template.pot`
contains the extracted messages. Compiled `.mo` files are bundled inside the
widget; they are generated and excluded from Git.

Run the following commands from the repository root. Python 3 and gettext
(`xgettext`, `msgmerge` and `msgfmt`) are required for the complete workflow.
The `kpac` helper is already included in the repository.

## Add or update a language

For a new language, copy `package/translate/template.pot` to
`package/translate/<locale>.po`, for example `es.po` or `pt_BR.po`. Set the catalog
headers for that locale and fill in the translations without changing message
identifiers. Submit the catalog through this fork's contribution workflow.

After changing translatable QML strings, extract messages, merge catalogs and
compile translations:

```bash
python3 ./kpac i18n
```

Review and commit changes to the template and catalogs. To check a catalog
without rebuilding the widget:

```bash
msgfmt --check --output-file=/dev/null package/translate/es.po
```

Replace `es.po` with the catalog being checked. Use the catalog itself to inspect
translation coverage. `python3 ./kpac i18n` prints current coverage without
overwriting this guide. Only translated, non-fuzzy messages are compiled for use;
untranslated messages fall back to English.

## Compile and preview

Compile existing catalogs without extracting or merging messages:

```bash
bash ./build --i18n-only
```

Build a complete package from those catalogs:

```bash
bash ./build --no-merge
```

Compiled files are placed under
`package/contents/locale/<locale>/LC_MESSAGES/plasma_applet_com.github.zren.tiledmenu.mo`.

Preview a language with Plasma 6's `plasmoidviewer` from `plasma-sdk`:

```bash
python3 ./kpac localetest es
```

`bash ./build` also performs extraction and merging, and stops if translation
sources have uncommitted changes. Use the explicit workflow above to review
catalog updates before packaging.

## Catalog review

Coverage against the current 118-message template, reviewed on 2026-10-11.
All 20 supported catalogs contain translations for every current message, with
no pending or fuzzy entries. This measures coverage; contributions improving
wording and regional terminology are welcome.
Run the extraction workflow again after changing source strings.

| Locale | Compiled translations | Pending |
| --- | ---: | ---: |
| `de` | 118 | 0 |
| `es` | 118 | 0 |
| `fa` | 118 | 0 |
| `fi` | 118 | 0 |
| `fr` | 118 | 0 |
| `he` | 118 | 0 |
| `hr` | 118 | 0 |
| `id` | 118 | 0 |
| `ja` | 118 | 0 |
| `ko` | 118 | 0 |
| `nl` | 118 | 0 |
| `pl` | 118 | 0 |
| `pt` | 118 | 0 |
| `pt_BR` | 118 | 0 |
| `ro` | 118 | 0 |
| `ru` | 118 | 0 |
| `sl` | 118 | 0 |
| `tr` | 118 | 0 |
| `zh_CN` | 118 | 0 |
| `zh_TW` | 118 | 0 |
