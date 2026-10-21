"""Contract tests for the public empty-channel site state."""

from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock


MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "build_site.py"
SPEC = importlib.util.spec_from_file_location("build_site", MODULE_PATH)
build_site = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(build_site)


class EmptyChannelTests(unittest.TestCase):
    def test_stable_fix_and_existing_versions_use_the_verified_archive(self):
        for channel, version, addon_version in (
            ('stable', '0.4.1', '0.4.1'),
            ('stable', '0.4.1-fix.1', '0.4.1-fix.1'),
            ('stable', '0.4.1-fix.10', '0.4.1-fix.10'),
            ('beta', '0.4.2-beta.1', '0.4.2'),
        ):
            with self.subTest(version=version), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                (root / channel).mkdir()
                tag = f'{channel}/v{version}'
                name = f'combine_tool_{version}.zip'
                url = f'{build_site.RELEASES}/download/{tag}/{name}'
                manifest = {
                    'schema': 'combine-tool-channel-manifest-v1', 'schema_version': 1,
                    'channel': channel, 'addon_version': addon_version,
                    'blender_min': [4, 4, 3], 'blender_max': [4, 5, 3],
                    'signature': {'algorithm': 'ed25519', 'value': 'test-signature'},
                    'archive': {'name': name, 'url': url, 'size': 100, 'sha256': 'a' * 64},
                }
                release = {
                    'tag_name': tag, 'draft': False, 'immutable': True, 'prerelease': channel == 'beta',
                    'html_url': f'{build_site.RELEASES}/tag/{tag}',
                    'assets': [
                        {'name': name, 'size': 100, 'browser_download_url': url},
                        {'name': 'channel-manifest.json', 'browser_download_url': 'https://example.test/manifest.json'},
                    ],
                }
                pointer = root / channel / 'manifest.json'
                pointer.write_text(json.dumps(manifest))
                with mock.patch.object(build_site, 'ROOT', root), mock.patch.object(build_site, 'get_json', side_effect=[release, manifest]):
                    result = build_site.public_release(channel)
                self.assertEqual(result['version'], version)
                self.assertEqual(result['archive_url'], url)
                pointer.write_text(json.dumps({**manifest, 'addon_version': '0.4.1-fix.99'}))
                with mock.patch.object(build_site, 'ROOT', root), self.assertRaises(ValueError):
                    build_site.public_release(channel)

    def test_missing_pointer_is_an_unpublished_channel(self):
        with tempfile.TemporaryDirectory() as directory, mock.patch.object(build_site, "ROOT", Path(directory)):
            self.assertIsNone(build_site.public_release("stable"))
            self.assertIsNone(build_site.public_release("beta"))

    def test_unpublished_channels_are_written_as_null(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            output = root / "site"
            with mock.patch.object(build_site, "ROOT", root), mock.patch("sys.argv", ["build_site.py", "--output", str(output)]):
                build_site.main()
            self.assertEqual((output / "releases.json").read_text(encoding="utf-8"), '{\n  "stable": null,\n  "beta": null\n}\n')


if __name__ == "__main__":
    unittest.main()
