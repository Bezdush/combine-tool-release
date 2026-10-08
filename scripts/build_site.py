"""Publish only verified public release fields from the channel pointers."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import urllib.request


REPOSITORY = "Bezdush/combine-tool-release"
RELEASES = f"https://github.com/{REPOSITORY}/releases"
API = f"https://api.github.com/repos/{REPOSITORY}"
ROOT = Path(__file__).resolve().parents[1]


def get_json(url: str) -> dict:
    request = urllib.request.Request(url, headers={"User-Agent": "combine-tool-pages", "Accept": "application/vnd.github+json"})
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.load(response)


def public_release(channel: str) -> dict | None:
    if channel not in {"stable", "beta"}:
        raise ValueError("Only public channels are allowed on Pages")
    pointer = ROOT / channel / "manifest.json"
    # A clean distribution repository has no channel pointer until the first
    # verified promotion.  Missing pointers are a normal empty state; malformed
    # pointers remain a hard failure below.
    if not pointer.is_file():
        return None
    manifest = json.loads(pointer.read_text(encoding="utf-8"))
    archive = manifest.get("archive", {})
    signature = manifest.get("signature", {})
    if (manifest.get("schema") != "combine-tool-channel-manifest-v1"
            or manifest.get("schema_version") != 1 or manifest.get("channel") != channel
            or signature.get("algorithm") != "ed25519" or not signature.get("value")
            or not isinstance(archive, dict)):
        raise ValueError("Invalid public channel pointer")
    for field in ("blender_min", "blender_max"):
        parts = manifest.get(field)
        if not isinstance(parts, list) or len(parts) != 3 or any(type(part) is not int or part < 0 for part in parts):
            raise ValueError("Invalid Blender compatibility range")
    if manifest["blender_min"] > manifest["blender_max"]:
        raise ValueError("Invalid Blender compatibility range")

    prefix = f"{RELEASES}/download/"
    url = archive.get("url", "")
    if not isinstance(url, str) or not url.startswith(prefix):
        raise ValueError("Archive URL is outside the release repository")
    tag, separator, filename = url[len(prefix):].rpartition("/")
    version_pattern = r"\d+\.\d+\.\d+" + (r"-beta\.[1-9]\d*" if channel == "beta" else "")
    match = re.fullmatch(rf"(?:{channel}/)?v({version_pattern})", tag)
    if not separator or not match:
        raise ValueError("Archive tag does not match its public channel")
    version = match.group(1)
    if (filename != f"combine_tool_{version}.zip" or archive.get("name") != filename
            or manifest.get("addon_version") != version.split("-")[0]
            or type(archive.get("size")) is not int or archive["size"] < 1
            or not re.fullmatch(r"[0-9a-f]{64}", archive.get("sha256", ""))):
        raise ValueError("Signed pointer has inconsistent archive metadata")

    release = get_json(f"{API}/releases/tags/{tag}")
    if (release.get("tag_name") != tag or release.get("draft")
            or release.get("immutable") is not True
            or release.get("prerelease") is not (channel == "beta")):
        raise ValueError("Channel does not point to a published immutable release")
    assets = {asset["name"]: asset for asset in release.get("assets", [])}
    zip_asset = assets.get(filename)
    manifest_asset = assets.get("channel-manifest.json")
    if (not zip_asset or zip_asset.get("size") != archive["size"]
            or zip_asset.get("browser_download_url") != url or not manifest_asset
            or get_json(manifest_asset["browser_download_url"]) != manifest):
        raise ValueError("Published release assets differ from the channel pointer")
    release_url = f"{RELEASES}/tag/{tag}"
    if release.get("html_url") != release_url:
        raise ValueError("Unexpected public release URL")
    return {
        "version": version,
        "release_url": release_url,
        "archive_url": url,
        "archive_name": filename,
        "blender_min": manifest["blender_min"],
        "blender_max": manifest["blender_max"],
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    releases = {channel: public_release(channel) for channel in ("stable", "beta")}
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "releases.json").write_text(json.dumps(releases, indent=2) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
