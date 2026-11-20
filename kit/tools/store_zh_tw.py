#!/usr/bin/env python3
"""zh-TW source-package build entry for ONE app of this repository, keeping the numeric Store version.

The head-unit updater supplies the SDK before invoking it; the author's build.py does the work. No language fallback,
no persistence agent. Each app reads its own catalog apps/<id>/zh-TW.json.
"""
import hashlib
import json
from pathlib import Path
import sys

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent.parent
EXPECTED = {
    'build.py': 'c1d9a2c11501ef5ff8a1bb56dd9f955b72738deb3f0c1896b51d6ab65f96ad42',
    'localize.py': 'a52ba86f1925b99051a7da5a0e1695766b622b33dd3850c32f5eeaaa9a73c923',
}


def main():
    present = sorted(p.name for p in (ROOT / 'apps').iterdir() if p.is_dir())
    args = sys.argv[1:]
    if len(args) not in (3, 4) or args[0] not in present or args[1:3] != ['--language', 'zh-TW'] or (len(args) == 4 and args[3] != '--preview-only'):
        raise SystemExit('Usage: store_zh_tw.py <app id> --language zh-TW [--preview-only]; no language fallback.')
    app = args[0]
    for name, digest in EXPECTED.items():
        if hashlib.sha256((TOOLS / name).read_bytes()).hexdigest() != digest:
            raise SystemExit('Builder compatibility check failed (' + name + '); rebuild the source package.')
    catalog = ROOT / 'apps' / app / 'zh-TW.json'
    if not catalog.is_file():
        raise SystemExit('Traditional-Chinese catalog is missing; no language fallback.')
    sys.path.insert(0, str(TOOLS))
    import localize
    original_version = localize.package_version
    localize.package_version = lambda version, language: version if language == 'zh-TW' else original_version(version, language)
    original_locale = localize.load_locale
    localize.load_locale = lambda language: json.loads(catalog.read_text(encoding='utf-8')) if language == 'zh-TW' else original_locale(language)
    import build
    print('%s: zh-TW; source package; SDK supplied by the head-unit updater' % app, flush=True)
    build.main()


if __name__ == '__main__':
    main()
