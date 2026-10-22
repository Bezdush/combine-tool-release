# Combine Tool for Blender

Combine Tool is a Blender add-on for non-destructive assembly of evaluated meshes while preserving the source scene.

Maintainers: see [FIRST_RELEASE.md](FIRST_RELEASE.md) before publishing the first STABLE build.

## Installation

Download the versioned ZIP from the [Combine Tool release page](https://bezdush.github.io/combine-tool-release/).

The page refreshes automatically after a public channel pointer changes. GitHub Actions also rebuilds it every two hours so a temporary Pages deployment failure does not leave download links stale indefinitely.

1. Download the versioned ZIP for the Stable release you want.
2. In Blender, open **Edit > Preferences > Add-ons > Install from Disk**.
3. Select the ZIP, install it, and enable the add-on.
4. Check that the release is compatible with your Blender version, and save your work before updating.

Stable fixes keep the base release number and add an ordered revision, such as
`0.4.1 Fix 1` (`stable/v0.4.1-fix.1`). Each fix has its own immutable Release and
ZIP. Combine Tool 0.4.1 introduces updater support for this revision format;
install that base version before using automatic fix updates.

## Report a problem

Report issues at [GitHub Issues](https://github.com/Bezdush/combine-tool-release/issues/new). Include the add-on version, Blender version, and steps to reproduce the problem. Remove private data from screenshots, files, and other attachments.
