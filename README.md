# Combine Tool release feed

This public repository is a delivery channel only. It contains signed pointers for public releases and never contains add-on source code, TEST builds, signing keys, access tokens, or user data.

## Public channels

| Channel | Purpose | Manifest |
| --- | --- | --- |
| `beta` | Opt-in public pre-release validation. | `beta/manifest.json` |
| `stable` | Approved releases for everyday work. | `stable/manifest.json` |

A missing manifest means that no release has been published for that channel yet. TEST builds are private to the maintainers and are never published here.

## Update trust model

Each published pointer conforms to [manifest.schema.json](manifest.schema.json) and is signed with Ed25519. The updater verifies that signature before accepting any field, then verifies the immutable release asset's size and SHA-256 before staging an update.

The ZIP is built once on the private release line, tested with Blender 4.4.3 and 4.5 LTS, then copied unchanged through BETA and STABLE. Release assets and tags are immutable. A rollback changes only a signed channel pointer; it never rewrites an asset.

## Repository scope

Allowed:

- `beta/manifest.json` and `stable/manifest.json`;
- immutable GitHub Release assets;
- this schema and delivery documentation.

Not allowed:

- add-on source;
- TEST assets or manifests;
- private keys, access tokens, or other credentials;
- user data.
