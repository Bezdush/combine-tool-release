"""Contract tests for the public empty-channel site state."""

from __future__ import annotations

import importlib.util
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
