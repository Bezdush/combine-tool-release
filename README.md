# Combine Tool public release feed

This public repository contains packaged releases and signed channel pointers for Combine Tool. It never contains add-on source code or signing credentials.

## Public channels

| Channel | Audience | Raw manifest |
| --- | --- | --- |
| `test` | Public experimental builds after main CI passes. | [test/manifest.json](test/manifest.json) |
| `beta` | Opt-in public pre-release validation. | [beta/manifest.json](beta/manifest.json) |
| `stable` | Approved releases for everyday work. | [stable/manifest.json](stable/manifest.json) |

Updater URLs use `https://raw.githubusercontent.com/Bezdush/combine-tool-release/main/<channel>/manifest.json`. A missing pointer means no build is currently published. TEST is public; there is no private TEST feed.

## Manifest contract

All three channels use the same `combine-tool-channel-manifest-v1` format in [manifest.schema.json](manifest.schema.json). [manifest.example.json](manifest.example.json) is illustrative only and its signature is not trusted.

The signature is Ed25519 over the canonical UTF-8 payload: the complete manifest object without `signature`, recursively sorted keys, compact JSON separators, no ASCII escaping, and one trailing LF. The source repository's `scripts/release_manifest.py` defines the canonical bytes and validation contract.

Each pointer binds channel, add-on version, build ID, commit SHA, Blender compatibility, immutable archive URL/name/size/SHA-256, notes and source release tag. Updater verifies the signature before trusting these fields and checks archive size and SHA-256 before staging.

## Build and promotion

The source workflow builds a candidate ZIP once, validates it, and tests those same bytes with Blender 4.4.3. TEST publishes that exact artifact after CI passes. Promotion copies the existing archive through `TEST → BETA → STABLE`; it never rebuilds.

Archive releases and tags are immutable. Channel manifest files are signed pointers and may be updated for promotion or rollback. Rollback changes only the pointer; it does not alter release assets. Never overwrite or delete a release asset.

## Repository scope

Allowed: signed channel pointers, immutable ZIP release assets and distribution documentation.

Not allowed: add-on source, private keys, access tokens, user data or unpublished credentials.
