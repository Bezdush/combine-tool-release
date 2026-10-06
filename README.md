# Combine Tool for Blender

[**Downloads and installation →**](https://bezdush.github.io/combine-tool-release/)

Choose **Stable** for everyday work or **Beta** for a preview. Download the `combine_tool_VERSION.zip` asset. GitHub’s automatic “Source code” archives contain this delivery website, not the add-on.

## Install

Keep the ZIP zipped. In Blender, open **Edit → Preferences → Add-ons → Install from Disk**, select the ZIP and enable Combine Tool. Use the Blender versions shown with your release. Save your work before updating.

[Report a problem](https://github.com/Bezdush/combine-tool-release/issues/new) with your add-on version, Blender version and steps to reproduce. Remove private data from attachments.

## Delivery contract

The signed `stable/manifest.json` and `beta/manifest.json` identify recommended downloads, including after a rollback. GitHub “latest” is not the source of truth. Missing manifests mean no verified release is available yet; no placeholders are published.

Stable uses `vX.Y.Z`; Beta uses `vX.Y.Z-beta.N` and is marked Pre-release. Assets are an immutable user ZIP and `channel-manifest.json`, the signed snapshot used for integrity and rollback. Human notes include changes, fixes, known limitations and tested Blender compatibility.

The page reads current pointers and loads stable history automatically. Browser UI does not verify signatures; the publisher and add-on updater do. Internal metadata stays inside the ZIP and signed manifest, with optional technical details on the page. Separate checksum/build-info sidecars are unnecessary.

`manifest.schema.json` remains the public updater contract. TEST stays private. This repository contains no add-on source tree, private keys, tokens or user data. Only the owner and controlled publisher write; visitors read and download.

GitHub Pages is enabled with **Source: GitHub Actions** and HTTPS. The page becomes available after this PR is merged. Public `main` is protected against force pushes/deletion, with PR review required for non-admins. The owner retains administrator bypass for the controlled publisher; no other collaborator currently has write access.
