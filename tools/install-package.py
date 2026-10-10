#!/usr/bin/python3
"""Install the applet, preserving unrecognized legacy packages for rollback."""
import json
import os
from pathlib import Path
import subprocess
import sys
from datetime import datetime
import uuid


def install(package, data_home):
    metadata = json.loads((package / 'metadata.json').read_text())
    namespace = metadata['KPlugin']['Id']
    if namespace != 'com.github.zren.tiledmenu':
        raise ValueError('Unexpected package ID; refusing to replace another widget')
    installed = data_home / 'plasma/plasmoids' / namespace
    backup = None
    legacy = False
    if installed.exists():
        if installed.is_symlink() or not installed.is_dir():
            raise ValueError(f'Refusing to replace a symlink or non-directory: {installed}')
        try:
            old_metadata = json.loads((installed / 'metadata.json').read_text())
        except (FileNotFoundError, json.JSONDecodeError):
            old_metadata = {}
        old_id = old_metadata.get('KPlugin', {}).get('Id', namespace)
        if old_id != namespace:
            raise ValueError('Installed metadata has an unexpected ID')
        legacy = (old_metadata.get('KPackageStructure') != 'Plasma/Applet'
                  or not (installed / 'contents/ui/main.qml').is_file())
        if legacy:
            stamp = datetime.now().strftime('%Y%m%d-%H%M%S') + '-' + uuid.uuid4().hex[:8]
            backup = data_home / 'tiledmenu/backups' / stamp / namespace
            backup.parent.mkdir(parents=True, exist_ok=False)
            installed.rename(backup)
            print(f'Legacy package backed up to: {backup}', flush=True)

    action = '--upgrade' if installed.exists() else '--install'
    try:
        subprocess.run(['kpackagetool6', '--type', 'Plasma/Applet', action, str(package)], check=True)
    except (subprocess.CalledProcessError, OSError):
        if legacy:
            # Preserve any incomplete new installation before restoring v45.
            if installed.exists():
                installed.rename(backup.parent / 'failed-new-package')
            backup.rename(installed)
            print('Installation failed; the original package was restored.', file=sys.stderr)
        raise


if __name__ == '__main__':
    package = Path(__file__).resolve().parents[1] / 'package'
    data_home = Path(os.environ.get('XDG_DATA_HOME') or Path.home() / '.local/share')
    try:
        install(package, data_home)
    except (OSError, ValueError, subprocess.CalledProcessError) as error:
        print(f'Installation failed: {error}', file=sys.stderr)
        sys.exit(1)
