#!/usr/bin/python3
"""Exercise legacy recovery and failure rollback with isolated XDG paths."""
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

root = Path(__file__).resolve().parents[1]
namespace = 'com.github.zren.tiledmenu'
with tempfile.TemporaryDirectory(prefix='tiledmenu-install-test-') as temporary:
    base = Path(temporary)
    data = base / 'data'
    config = base / 'config'
    config.mkdir()
    settings = config / 'plasma-org.kde.plasma.desktop-appletsrc'
    settings.write_text('[Containments][1][Applets][7]\nplugin=' + namespace + '\n[Containments][1][Applets][7][Configuration][General]\ntileModel=existing-layout\nsidebarShortcuts=existing-shortcuts\n')
    digest = hashlib.sha256(settings.read_bytes()).digest()
    installed = data / 'plasma/plasmoids' / namespace

    def legacy_fixture():
        (installed / 'contents/ui').mkdir(parents=True)
        (installed / 'metadata.json').write_text(json.dumps({
            'KPlugin': {'Id': namespace, 'Version': '45', 'ServiceTypes': ['Plasma/Applet']},
            'X-Plasma-MainScript': 'ui/Main.qml',
        }))
        (installed / 'contents/ui/Main.qml').write_text('legacy package marker')

    env = dict(os.environ, XDG_DATA_HOME=str(data), XDG_CONFIG_HOME=str(config),
               XDG_CACHE_HOME=str(base / 'cache'), QT_QPA_PLATFORM='offscreen', KDE_DEBUG='1')
    legacy_fixture()
    subprocess.run(['bash', str(root / 'install')], env=env, check=True)
    backups = list((data / 'tiledmenu/backups').glob('*/' + namespace))
    assert len(backups) == 1
    assert (backups[0] / 'contents/ui/Main.qml').read_text() == 'legacy package marker'
    assert json.loads((installed / 'metadata.json').read_text())['KPackageStructure'] == 'Plasma/Applet'
    subprocess.run(['bash', str(root / 'install')], env=env, check=True)
    subprocess.run(['bash', str(root / 'uninstall')], env=env, check=True)
    assert not installed.exists()
    assert hashlib.sha256(settings.read_bytes()).digest() == digest

    legacy_fixture()
    fake_bin = base / 'bin'
    fake_bin.mkdir()
    command = fake_bin / 'kpackagetool6'
    command.write_text('#!/bin/sh\nexit 1\n')
    command.chmod(0o755)
    env['PATH'] = str(fake_bin) + os.pathsep + env['PATH']
    failed = subprocess.run(['bash', str(root / 'install')], env=env)
    assert failed.returncode != 0
    assert (installed / 'contents/ui/Main.qml').read_text() == 'legacy package marker'
    assert hashlib.sha256(settings.read_bytes()).digest() == digest
print('PASS: legacy replacement, package backup, repeat upgrade, removal, failure rollback and unchanged panel settings.')
