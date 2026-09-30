# Combine Tool public release feed

This public repository contains only distribution metadata and packaged public releases for **Combine Tool**. It never contains the add-on source code.

## Public release channels

| Channel | Intended audience | Manifest URL |
| --- | --- | --- |
| `stable` | Public releases approved for everyday work. | `stable/manifest.json` |
| `beta` | Opt-in public pre-release validation. May contain unfinished features. | `beta/manifest.json` |

The updater must never switch channels by itself. A missing channel manifest means that channel currently has no published build.

The raw URL pattern is:

`https://raw.githubusercontent.com/Bezdush/combine-tool-release/main/<channel>/manifest.json`

## Test builds

The `test` directory is a public marker only. Development/test builds, their manifests, and their archives are deliberately **not** published from this repository. They use a separate private development feed.

## Publication contract

- Current manifest format: `schema_version: 1`.
- A release is published atomically: its ZIP, `manifest.json`, and optional notes must appear in the same commit.
- The archive must be verified by SHA-256 before staging.
- The manifest is detached-signed with Ed25519. The signature covers the canonical JSON payload described below.
- A build is installed only after Blender is closed/restarted; the previous installed copy remains available for rollback.
- Existing published archives and manifests are immutable. Corrections use a new version/build ID.

### Signature payload

The signature covers the UTF-8 bytes of the object formed by the top-level fields `schema_version`, `channel`, `release`, `archive`, and `integrity`. Serialization is canonical JSON: recursively sorted keys, compact separators `,` and `:`, and UTF-8 without ASCII escaping. The `signature` object itself is excluded.

See [manifest.schema.json](manifest.schema.json) for the machine-readable contract and [manifest.example.json](manifest.example.json) for a non-publishable example.

## Repository scope

Allowed: signed beta/stable manifests, their ZIP release assets, release notes, and this distribution documentation.

Not allowed: add-on source, development/test builds, Blender scene files, test scenes, private keys, personal access tokens, or user data.
